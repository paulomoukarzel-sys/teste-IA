"""
Migração de registros — Controle de Prazos
Limpa compromisso, resumo e partes dos registros existentes.
Pode ser executado múltiplas vezes (idempotente).
"""
import re, sqlite3, sys, os
sys.stdout.reconfigure(encoding='utf-8')

DB = os.path.join(os.path.dirname(__file__), "prazos.db")

# ── Padrões de ruído a remover do resumo ──────────────────────────────
_RUIDO_RESUMO = re.compile(
    r'advogado\s+de\s+origem[^\n]{0,150}\n?'
    r'|\(login:[^\)]{0,40}\)[^\n]{0,80}\n?'
    r'|código\s+da\s+publicação\s+\d+[^\n]{0,60}\n?'
    r'|sistema\s+eproc[^\n]{0,80}\n?'
    r'|p[aá]gina\s+\d+[^\n]{0,30}\n?'
    r'|tribunal\s+de\s+justiça[^\n]{0,80}\n?'
    r'|poder\s+judiciário[^\n]{0,80}\n?'
    r'|diário\s+(?:da\s+)?(?:justiça|eletrônico)[^\n]{0,100}\n?'
    r'|(?:adv\.|advogado[s]?\s*\()[^\n]{0,80}\n?'
    r'|\bSC\d{5,6}\b[^\n]{0,30}\n?'
    r'|não\s+responda[^\n]{0,80}\n?'
    r'|mensagem\s+automática[^\n]{0,60}\n?',
    re.IGNORECASE
)

_CORTA_PARTE = re.compile(
    r'\s+(?:advogado[s]?|adv\.|oab|login|sc\d{4,6}|\(sc|\d{7}-\d{2})',
    re.IGNORECASE
)

def _limpar_partes_texto(partes_str):
    """Remove 'Advogado(s)...' e ruído dos nomes de partes."""
    if not partes_str:
        return partes_str
    # Separa os polos pelo "×" ou "X"
    polos = re.split(r'\s*[×X]\s*', partes_str)
    limpos = []
    for polo in polos:
        # Remove prefixos de polo (EXEQUENTE, APELANTE, etc.)
        polo = re.sub(
            r'^(?:exequente|executado[a]?|apelante|apelado[a]?|autor[a]?|réu|ré|requerente|requerido[a]?|reclamante|reclamado[a]?|impetrante|impetrado[a]?|agravante|agravado[a]?)\s+',
            '', polo, flags=re.IGNORECASE
        ).strip()
        # Corta a partir de "Advogado(s)", OAB, código SC
        corte = _CORTA_PARTE.search(polo)
        if corte:
            polo = polo[:corte.start()].strip()
        if len(polo) > 3:
            limpos.append(polo[:60])
    return ' × '.join(limpos) if limpos else ""


def _limpar_resumo(resumo):
    """Remove ruído institucional do resumo já migrado."""
    if not resumo:
        return resumo

    # Remove padrões de ruído
    texto = _RUIDO_RESUMO.sub('', resumo)

    # Se a linha "Teor:" ficou vazia ou só tem ruído, remove
    linhas_out = []
    for linha in texto.split('\n'):
        ls = linha.strip()
        if ls.startswith('Teor:'):
            conteudo = ls[5:].strip()
            # Teor com menos de 20 chars ou que começa com padrão de ruído — descarta
            if len(conteudo) < 20 or re.match(
                r'(advogado|login|sua conta|prezado|código|sistema|página)',
                conteudo, re.IGNORECASE
            ):
                continue
        linhas_out.append(ls)

    # Remove linhas vazias excessivas e limpa
    resultado = []
    prev_blank = False
    for l in linhas_out:
        if not l:
            if not prev_blank and resultado:
                resultado.append('')
            prev_blank = True
        else:
            resultado.append(l)
            prev_blank = False

    # Remove trailing blanks
    while resultado and not resultado[-1]:
        resultado.pop()

    return '\n'.join(resultado)


def _migrar_compromisso(compromisso, resumo=""):
    """Converte '[TRIBUNAL] Intimação — ...' para ação concreta."""
    if not compromisso or not compromisso.startswith('['):
        return None  # já no novo formato

    texto = f"{compromisso} {resumo}".lower()

    acoes = [
        (r'cita[çc][aã]o|citado|foi\s+citad[ao]',             "Elaborar contestação no prazo legal"),
        (r'audi[eê]ncia\s+de\s+(?:instrução|conciliação|julgamento)', "Preparar para audiência"),
        (r'sess[aã]o\s+de\s+julgamento|pauta\s+de\s+julgamento', "Preparar para sessão de julgamento"),
        (r'audi[eê]ncia',                                       "Preparar para audiência"),
        (r'senten[çc]a',                                        "Analisar sentença e verificar cabimento de recurso (prazo: 15 dias úteis)"),
        (r'ac[oó]rd[aã]o',                                      "Analisar acórdão e verificar cabimento de REsp/RE/ED (prazo: 15 dias úteis)"),
        (r'embargos\s+de\s+declara[çc][aã]o',                  "Elaborar embargos de declaração (prazo: 5 dias úteis)"),
        (r'contrarraz[õo]es',                                   "Elaborar contrarrazões ao recurso interposto (prazo: 15 dias úteis)"),
        (r'agravo\s+de\s+instrumento',                          "Elaborar resposta ao agravo de instrumento"),
        (r'manifeste[-\s]se|manifestar[-\s]se',                 "Elaborar manifestação no prazo fixado"),
        (r'dilig[eê]ncia',                                      "Cumprir diligência no prazo fixado"),
        (r'cumprimento\s+de\s+senten[çc]a|execu[çc][aã]o',    "Verificar cumprimento de sentença / providenciar defesa na execução"),
        (r'per[ií]cia|perito',                                  "Acompanhar perícia e verificar necessidade de assistente técnico"),
        (r'despacho',                                           "Verificar determinação do despacho e cumprir no prazo"),
        (r'decis[aã]o\s+interlocut[oó]ria|decis[aã]o\s+monocr[aá]tica', "Analisar decisão e verificar cabimento de agravo de instrumento"),
        (r'movimenta[çc][aã]o',                                 "Verificar movimentação processual e adotar providência cabível"),
        (r'intima[çc][aã]o|intimad[ao]|nova\s+intima[çc][aã]o', "Analisar intimação e adotar providência cabível no prazo"),
    ]

    for pattern, acao in acoes:
        if re.search(pattern, texto, re.IGNORECASE):
            return acao

    return "Verificar ato processual e adotar providência cabível"


def _tribunal_do_compromisso(compromisso, tribunal_atual):
    if tribunal_atual:
        return None
    if not compromisso or not compromisso.startswith('['):
        return None
    m = re.match(r'\[([^\]]+)\]', compromisso)
    return m.group(1).strip() if m else None


def migrar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM prazos").fetchall()

    atualizados = 0
    for r in rows:
        updates = {}

        # 1. Compromisso (apenas se ainda no formato antigo)
        novo_comp = _migrar_compromisso(r["compromisso"], r["resumo"] or "")
        if novo_comp:
            updates["compromisso"] = novo_comp

        # 2. Tribunal (apenas se não preenchido)
        novo_trib = _tribunal_do_compromisso(r["compromisso"], r["tribunal"])
        if novo_trib:
            updates["tribunal"] = novo_trib

        # 3. Resumo — limpa ruído em TODOS os registros
        resumo_atual = r["resumo"] or ""
        resumo_limpo = _limpar_resumo(resumo_atual)
        if resumo_limpo != resumo_atual:
            updates["resumo"] = resumo_limpo

        # 4. Partes — limpa ruído em TODOS os registros
        partes_atual = r["partes"] or ""
        partes_limpas = _limpar_partes_texto(partes_atual)
        if partes_limpas != partes_atual:
            updates["partes"] = partes_limpas

        if updates:
            fields = ", ".join(f"{k}=?" for k in updates)
            vals   = list(updates.values()) + [r["id"]]
            conn.execute(f"UPDATE prazos SET {fields} WHERE id=?", vals)
            print(f"  [{r['id']}] {(r['cliente'] or '')[:35]}")
            for k, v in updates.items():
                print(f"       {k}: {str(v)[:80]}")
            atualizados += 1

    conn.commit()
    conn.close()
    print(f"\n{atualizados} registro(s) atualizado(s) de {len(rows)} total.")

if __name__ == "__main__":
    print("Migrando registros...\n")
    migrar()
