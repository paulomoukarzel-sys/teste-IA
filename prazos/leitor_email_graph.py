"""
Leitor de E-mail via Microsoft Graph API — Controle de Prazos
Gastão da Rosa & Moukarzel — Advogados Associados

Usa autenticação por dispositivo (Device Flow):
- Na primeira execução: abre o browser uma vez para autorizar
- Nas próximas: usa token salvo automaticamente (sem interação)

Acesso SOMENTE LEITURA — não envia, responde nem modifica e-mails.
"""
import json, os, re, sys, time, logging, requests
from datetime import date, datetime, timedelta
from msal import PublicClientApplication, SerializableTokenCache

sys.stdout.reconfigure(encoding='utf-8')

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "leitor_email.log"),
                            encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)

# ── Configuração ─────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(__file__)
TOKEN_FILE  = os.path.join(BASE_DIR, "graph_token.json")
DB_FILE     = os.path.join(BASE_DIR, "prazos.db")
API_BASE    = "http://localhost:5001"

# App ID público da Microsoft para acesso a contas pessoais (Hotmail/Outlook.com)
# Este é o client_id oficial para apps de desktop/CLI da Microsoft
CLIENT_ID   = "14d82eec-204b-4c2f-b7e8-296a70dab67e"  # Microsoft Graph Explorer (público, contas pessoais)
AUTHORITY   = "https://login.microsoftonline.com/consumers"
SCOPES      = ["Mail.Read"]  # Somente leitura

GRAPH_BASE  = "https://graph.microsoft.com/v1.0"

# ── Importações do leitor_email.py ───────────────────────────────────
# Reutiliza toda a lógica de parser de tribunais já construída
sys.path.insert(0, BASE_DIR)
try:
    from leitor_email import (
        TRIBUNAIS, TIPOS_ATO, RE_PROCESSO, RE_DATA, RE_DATA_EXTENSO, MESES_PT,
        identificar_tribunal, extrair_processo, extrair_tipo_e_prazo,
        extrair_nome_cliente, construir_compromisso, construir_resumo,
        init_email_db, ja_processado, marcar_processado, enviar_prazo,
        strip_html
    )
    log.info("Parser de tribunais carregado de leitor_email.py")
except ImportError as e:
    log.error(f"Não foi possível importar leitor_email.py: {e}")
    sys.exit(1)

# ── Autenticação Microsoft Graph ──────────────────────────────────────

def get_token_cache():
    cache = SerializableTokenCache()
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, encoding="utf-8") as f:
            cache.deserialize(f.read())
    return cache

def save_token_cache(cache):
    if cache.has_state_changed:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(cache.serialize())

def autenticar():
    """Autentica via Device Flow — abre browser uma vez."""
    cache = get_token_cache()
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    # Tenta usar token existente primeiro
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            save_token_cache(cache)
            log.info("Token reutilizado (sem necessidade de login).")
            return result["access_token"]

    # Device Flow — pede ao usuário para abrir o browser
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception(f"Falha ao iniciar Device Flow: {flow}")

    print("\n" + "═" * 60)
    print("  AUTORIZAÇÃO NECESSÁRIA — apenas na primeira vez")
    print("═" * 60)
    print(f"\n  1. Abra: {flow['verification_uri']}")
    print(f"  2. Digite o código: {flow['user_code']}")
    print(f"\n  Aguardando autorização...\n")

    # Abre o browser automaticamente
    import webbrowser
    webbrowser.open(flow["verification_uri"])

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise Exception(f"Falha na autenticação: {result.get('error_description', result)}")

    save_token_cache(cache)
    log.info("Autenticação concluída e token salvo.")
    return result["access_token"]

# ── Microsoft Graph — leitura de e-mails ─────────────────────────────

def buscar_emails_tribunais(token, limite=50):
    """Busca e-mails de tribunais via Graph API usando search."""
    headers = {"Authorization": f"Bearer {token}"}
    emails = []
    ids_ja = set()

    # Termos de busca — cobre domínios .jus.br e palavras-chave processuais
    termos = [
        "jus.br",
        "intimação",
        "citação",
        "prazo processual",
        "e-proc",
        "pje projudi",
        "audiência judicial",
        "decisão judicial",
        "despacho judicial",
    ]

    data_inicio = "2026-03-10T00:00:00Z"

    for termo in termos:
        # Graph não permite $search + $filter juntos; usa $search e filtra localmente por data
        url = (
            f"{GRAPH_BASE}/me/messages"
            f"?$top=50"
            f"&$select=id,subject,from,receivedDateTime,body,isRead"
            f"&$search=\"{termo}\""
        )
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            for msg in resp.json().get("value", []):
                if msg["id"] not in ids_ja:
                    # Filtra localmente por data >= 10/03/2026
                    received = msg.get("receivedDateTime", "")
                    if received and received < "2026-03-10T00:00:00Z":
                        continue
                    emails.append(msg)
                    ids_ja.add(msg["id"])
        elif resp.status_code != 400:
            log.warning(f"Busca '{termo}' retornou {resp.status_code}: {resp.text[:100]}")

    log.info(f"Encontrados {len(emails)} e-mails candidatos de tribunais")
    return emails[:limite]

def processar_email_graph(msg):
    """Processa mensagem do Graph API e retorna dados extraídos ou None."""
    msg_id    = msg.get("id", "")
    assunto   = msg.get("subject", "") or ""
    remetente = msg.get("from", {}).get("emailAddress", {}).get("address", "") or ""
    data_str  = msg.get("receivedDateTime", "")
    body_obj  = msg.get("body", {})
    body_raw  = body_obj.get("content", "") or ""

    # Converte HTML para texto se necessário
    content_type = body_obj.get("contentType", "text")
    corpo = strip_html(body_raw) if content_type == "html" else body_raw

    # Data do e-mail
    try:
        data_email = datetime.fromisoformat(data_str.replace("Z", "+00:00")).date()
    except Exception:
        data_email = date.today()

    texto_completo = f"{remetente} {assunto} {corpo}"
    texto_lower    = texto_completo.lower()

    tribunal = identificar_tribunal(remetente, assunto, corpo)
    if not tribunal:
        return None

    processo  = extrair_processo(texto_completo)
    tipo, data_prazo = extrair_tipo_e_prazo(texto_lower, data_email)
    cliente   = extrair_nome_cliente(assunto, corpo, processo)

    tipo_ato_raw = None
    for kw in TIPOS_ATO:
        if kw in texto_lower:
            tipo_ato_raw = kw
            break

    compromisso = construir_compromisso(tipo_ato_raw, texto_lower)
    resumo      = construir_resumo(tribunal, assunto, corpo, processo, data_email)

    from leitor_email import _extrair_partes
    partes_list = _extrair_partes(corpo)
    partes      = " × ".join(partes_list) if partes_list else ""

    return {
        "msg_id":      msg_id,
        "tribunal":    tribunal,
        "partes":      partes,
        "data_prazo":  data_prazo,
        "cliente":     cliente,
        "compromisso": compromisso,
        "tipo":        tipo,
        "resumo":      resumo,
    }

# ── Sincronização principal ───────────────────────────────────────────

def sincronizar_graph():
    """Autentica e sincroniza e-mails de tribunais."""
    init_email_db()
    novos = ignorados = erros = 0

    try:
        token = autenticar()
    except Exception as e:
        msg = str(e)
        log.error(f"Falha na autenticação: {msg}")
        return {"novos": 0, "ignorados": 0, "erros": 1, "msg": msg}

    try:
        emails = buscar_emails_tribunais(token)
        log.info(f"Total de e-mails candidatos: {len(emails)}")

        for msg in emails:
            msg_id = msg.get("id", "")
            if ja_processado(msg_id):
                ignorados += 1
                continue

            dados = processar_email_graph(msg)
            if dados is None:
                marcar_processado(msg_id, "nao_tribunal")
                ignorados += 1
                continue

            log.info(f"Processando: [{dados['tribunal']}] {dados['compromisso'][:60]}")
            ok = enviar_prazo(
                dados["data_prazo"],
                dados["cliente"],
                dados["compromisso"],
                dados["tipo"],
                dados["resumo"],
                dados.get("tribunal", ""),
                dados.get("partes", ""),
            )
            marcar_processado(msg_id, "ok" if ok else "erro_api")
            if ok:
                novos += 1
            else:
                erros += 1

    except Exception as e:
        log.error(f"Erro durante sincronização: {e}")
        erros += 1

    resultado = {
        "novos":     novos,
        "ignorados": ignorados,
        "erros":     erros,
        "msg":       f"{novos} prazo(s) cadastrado(s), {ignorados} ignorado(s), {erros} erro(s)."
    }
    log.info(resultado["msg"])
    return resultado

# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    resultado = sincronizar_graph()
    print(f"\n{resultado['msg']}")
