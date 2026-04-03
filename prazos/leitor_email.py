"""
Leitor de E-mail — Controle de Prazos
Gastão da Rosa & Moukarzel — Advogados Associados

Monitora a caixa de entrada via IMAP e identifica e-mails de
qualquer tribunal brasileiro, extraindo dados para o sistema
de controle de prazos (localhost:5001).

Suporte: Gmail, Outlook/Office365, qualquer servidor IMAP.
"""
import imaplib
import email
import email.header
import json
import os
import re
import sqlite3
import sys
import time
import logging
import requests
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

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
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "email_config.json")
DB_FILE     = os.path.join(os.path.dirname(__file__), "prazos.db")
API_BASE    = "http://localhost:5001"

# ── Tribunais brasileiros reconhecidos ───────────────────────────────
TRIBUNAIS = {
    # Superiores
    "stj.jus.br":      "STJ",
    "stf.jus.br":      "STF",
    "tst.jus.br":      "TST",
    "tse.jus.br":      "TSE",
    "stm.jus.br":      "STM",
    "cjf.jus.br":      "CJF",
    "cnj.jus.br":      "CNJ",
    # TRFs
    "trf1.jus.br":     "TRF1",
    "trf2.jus.br":     "TRF2",
    "trf3.jus.br":     "TRF3",
    "trf4.jus.br":     "TRF4",
    "trf5.jus.br":     "TRF5",
    "trf6.jus.br":     "TRF6",
    # Justiça Federal por estado
    "jfsc.jus.br":     "JFSC",
    "jfpr.jus.br":     "JFPR",
    "jfrs.jus.br":     "JFRS",
    "jfsp.jus.br":     "JFSP",
    # TJs
    "tjsc.jus.br":     "TJSC",
    "tjsp.jus.br":     "TJSP",
    "tjrs.jus.br":     "TJRS",
    "tjpr.jus.br":     "TJPR",
    "tjmg.jus.br":     "TJMG",
    "tjrj.jus.br":     "TJRJ",
    "tjba.jus.br":     "TJBA",
    "tjgo.jus.br":     "TJGO",
    "tjms.jus.br":     "TJMS",
    "tjmt.jus.br":     "TJMT",
    "tjpa.jus.br":     "TJPA",
    "tjpe.jus.br":     "TJPE",
    "tjce.jus.br":     "TJCE",
    "tjma.jus.br":     "TJMA",
    "tjpi.jus.br":     "TJPI",
    "tjal.jus.br":     "TJAL",
    "tjse.jus.br":     "TJSE",
    "tjrn.jus.br":     "TJRN",
    "tjpb.jus.br":     "TJPB",
    "tjam.jus.br":     "TJAM",
    "tjpa.jus.br":     "TJPA",
    "tjro.jus.br":     "TJRO",
    "tjrr.jus.br":     "TJRR",
    "tjap.jus.br":     "TJAP",
    "tjto.jus.br":     "TJTO",
    "tjac.jus.br":     "TJAC",
    "tjdf.jus.br":     "TJDF",
    "tjdft.jus.br":    "TJDFT",
    "tjrr.jus.br":     "TJRR",
    # TRTs
    "trt1.jus.br":     "TRT1",
    "trt2.jus.br":     "TRT2",
    "trt3.jus.br":     "TRT3",
    "trt4.jus.br":     "TRT4",
    "trt5.jus.br":     "TRT5",
    "trt6.jus.br":     "TRT6",
    "trt7.jus.br":     "TRT7",
    "trt8.jus.br":     "TRT8",
    "trt9.jus.br":     "TRT9",
    "trt10.jus.br":    "TRT10",
    "trt11.jus.br":    "TRT11",
    "trt12.jus.br":    "TRT12",
    "trt13.jus.br":    "TRT13",
    "trt14.jus.br":    "TRT14",
    "trt15.jus.br":    "TRT15",
    "trt16.jus.br":    "TRT16",
    "trt17.jus.br":    "TRT17",
    "trt18.jus.br":    "TRT18",
    "trt19.jus.br":    "TRT19",
    "trt20.jus.br":    "TRT20",
    "trt21.jus.br":    "TRT21",
    "trt22.jus.br":    "TRT22",
    "trt23.jus.br":    "TRT23",
    "trt24.jus.br":    "TRT24",
    # Portais eletrônicos
    "eproc.jus.br":    "e-Proc",
    "pje.jus.br":      "PJe",
    "projudi.jus.br":  "PROJUDI",
    # Genérico (qualquer .jus.br não mapeado)
    "jus.br":          "Tribunal",
}

# ── Padrões de extração ───────────────────────────────────────────────
# Número CNJ: 0000001-00.0000.0.00.0000
RE_PROCESSO = re.compile(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}')

# Palavras-chave para tipo de ato → tipo de compromisso
TIPOS_ATO = {
    "audiência":      ("audiencia", 1),   # (tipo, prazo_dias_padrao)
    "julgamento":     ("audiencia", 1),
    "sessão":         ("audiencia", 1),
    "intimação":      ("prazo",    15),
    "intimacao":      ("prazo",    15),
    "citação":        ("prazo",    15),
    "prazo":          ("prazo",    15),
    "recurso":        ("prazo",    15),
    "contrarraz":     ("prazo",    15),
    "embargos":       ("prazo",    15),
    "manifestação":   ("prazo",    15),
    "manifestacao":   ("prazo",    15),
    "petição":        ("peticao",  15),
    "peticao":        ("peticao",  15),
    "despacho":       ("prazo",    15),
    "acórdão":        ("prazo",    15),
    "acordao":        ("prazo",    15),
    "sentença":       ("prazo",    15),
    "sentenca":       ("prazo",    15),
    "decisão":        ("prazo",    15),
    "decisao":        ("prazo",    15),
    "diligência":     ("diligencia", 5),
    "diligencia":     ("diligencia", 5),
    "reunião":        ("reuniao",   1),
    "reuniao":        ("reuniao",   1),
}

# Padrões de data no corpo do e-mail
RE_DATA = re.compile(
    r'(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{2,4})'   # dd/mm/aaaa ou dd-mm-aaaa
    r'|(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})',    # aaaa-mm-dd
)

MESES_PT = {
    "janeiro":1,"fevereiro":2,"março":3,"marco":3,"abril":4,
    "maio":5,"junho":6,"julho":7,"agosto":8,"setembro":9,
    "outubro":10,"novembro":11,"dezembro":12,
}
RE_DATA_EXTENSO = re.compile(
    r'(\d{1,2})\s+de\s+(' + '|'.join(MESES_PT.keys()) + r')\s+de\s+(\d{4})',
    re.IGNORECASE
)

# ── Utilidades ───────────────────────────────────────────────────────

class HTMLStripper(HTMLParser):
    """Converte HTML para texto preservando quebras de linha em tags de bloco."""
    BLOCK_TAGS = {'p','div','br','tr','td','th','li','h1','h2','h3','h4','h5','h6',
                  'blockquote','pre','section','article','header','footer'}
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.BLOCK_TAGS:
            self.fed.append('\n')
    def handle_endtag(self, tag):
        if tag.lower() in self.BLOCK_TAGS:
            self.fed.append('\n')
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        texto = ''.join(self.fed)
        # Colapsa múltiplas quebras e espaços
        texto = re.sub(r'[ \t]+', ' ', texto)
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        return texto.strip()

def strip_html(html_text):
    s = HTMLStripper()
    try:
        s.feed(html_text)
        return s.get_data()
    except Exception:
        return html_text

def decode_header_value(raw):
    """Decodifica cabeçalhos de e-mail (charset variado)."""
    parts = email.header.decode_header(raw or "")
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return " ".join(result)

def get_email_body(msg):
    """Extrai texto plano do e-mail (preferindo text/plain)."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = part.get("Content-Disposition", "")
            if ct == "text/plain" and "attachment" not in cd:
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="replace")
            elif ct == "text/html" and "attachment" not in cd and not body:
                charset = part.get_content_charset() or "utf-8"
                html = part.get_payload(decode=True).decode(charset, errors="replace")
                body += strip_html(html)
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            raw = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/html":
                body = strip_html(raw)
            else:
                body = raw
    return body

# ── Identificação de tribunal ─────────────────────────────────────────

def identificar_tribunal(remetente, assunto, corpo):
    """Retorna nome do tribunal ou None se não for e-mail de tribunal."""
    texto = f"{remetente} {assunto} {corpo}".lower()
    # Verifica remetente primeiro (mais confiável)
    for dominio, nome in sorted(TRIBUNAIS.items(), key=lambda x: -len(x[0])):
        if dominio in texto:
            return nome
    # Fallback: keywords no assunto/corpo
    keywords = ["tribunal", "juízo", "vara ", "câmara", "turma", "plenário",
                "intimação", "citação", "processo n.", "autos do processo",
                "e-proc", "pje", "projudi", "despacho", "decisão judicial"]
    for kw in keywords:
        if kw in texto:
            return "Tribunal"
    return None

# ── Extração de dados ─────────────────────────────────────────────────

def extrair_processo(texto):
    """Extrai número CNJ do texto."""
    m = RE_PROCESSO.search(texto)
    return m.group(0) if m else None

def extrair_tipo_e_prazo(texto_lower, data_email):
    """Infere tipo do compromisso e calcula prazo."""
    tipo = "prazo"
    dias = 15
    for kw, (t, d) in TIPOS_ATO.items():
        if kw in texto_lower:
            tipo = t
            dias = d
            break

    # Para audiências/sessões, tenta encontrar a data do ato no corpo
    data_ato = extrair_data_ato(texto_lower)
    if data_ato and tipo == "audiencia":
        return tipo, data_ato

    # Para prazos, calcula a partir da data do e-mail
    data_base = data_email or date.today()
    data_prazo = data_base + timedelta(days=dias)
    # Pula fins de semana
    while data_prazo.weekday() >= 5:
        data_prazo += timedelta(days=1)
    return tipo, data_prazo

def extrair_data_ato(texto):
    """Tenta extrair data explícita de audiência/sessão do corpo."""
    # Formato extenso: "10 de abril de 2026"
    m = RE_DATA_EXTENSO.search(texto)
    if m:
        dia, mes_str, ano = m.group(1), m.group(2).lower(), m.group(3)
        mes = MESES_PT.get(mes_str)
        if mes:
            try:
                return date(int(ano), mes, int(dia))
            except ValueError:
                pass
    # Formato numérico: dd/mm/aaaa
    for m in RE_DATA.finditer(texto):
        g = m.groups()
        if g[0]:  # dd/mm/aaaa
            d, mo, y = g[0], g[1], g[2]
            if len(y) == 2:
                y = "20" + y
            try:
                return date(int(y), int(mo), int(d))
            except ValueError:
                pass
        elif g[3]:  # aaaa-mm-dd
            y, mo, d = g[3], g[4], g[5]
            try:
                return date(int(y), int(mo), int(d))
            except ValueError:
                pass
    return None

def extrair_nome_cliente(assunto, corpo, processo):
    """Tenta extrair nome do cliente do e-mail."""
    # Padrões: "Parte: João Silva", "Requerente: ...", "Autor: ..."
    padroes = [
        r'(?:parte|requerente|autor|reclamante|impetrante|agravante|apelante)\s*[:\-]\s*([A-ZÀ-Ú][a-zA-ZÀ-ú\s]{5,50})',
        r'(?:em nome de|representando|cliente)\s*[:\-]?\s*([A-ZÀ-Ú][a-zA-ZÀ-ú\s]{5,50})',
    ]
    texto = f"{assunto} {corpo}"
    for pat in padroes:
        m = re.search(pat, texto, re.IGNORECASE)
        if m:
            nome = m.group(1).strip()
            if len(nome) > 3:
                return nome[:60]
    # Se tem número de processo, usa como referência
    if processo:
        return f"Processo {processo}"
    return "Cliente a identificar"

# ── Ruído a remover do corpo da intimação ────────────────────────────
_RUIDO_PATTERNS = [
    # Cabeçalhos institucionais
    r'(?:tribunal|juízo|vara|câmara|turma|seção|subseção|fórum|comarca)[^\n]{0,120}\n',
    r'(?:poder judiciário|justiça federal|justiça estadual)[^\n]{0,80}\n',
    # Identificação do advogado destinatário (não é teor)
    r'advogado\s+de\s+origem[^\n]{0,120}\n?',
    r'\(login:\s*\w+\s*\w*\)[^\n]{0,80}\n?',
    r'código\s+da\s+publicação\s+\d+[^\n]{0,60}\n?',
    r'sistema\s+eproc[^\n]{0,80}\n?',
    r'p[aá]gina\s+\d+[^\n]{0,30}\n?',
    # Dados do diário / publicação
    r'diário\s+(?:da\s+)?(?:justiça|eletrônico|oficial)[^\n]{0,100}\n?',
    r'(?:edição|caderno|seção)\s+n[º°.]?\s*\d+[^\n]{0,60}\n?',
    r'publicad[ao]\s+em[^\n]{0,40}\n?',
    r'data\s+da\s+(?:disponibilização|publicação)[^\n]{0,40}',
    # Dados de advogados
    r'(?:adv\.|advogado[s]?[:\s\(]|dr\.|dra\.|procurador[a]?)[^\n]{0,80}\n?',
    r'\bSC\d{5,6}\b[^\n]{0,30}\n?',
    r'oab[/\s]\w+\s*\d+[^\n]{0,30}\n?',
    # Rodapés e avisos
    r'este\s+e-?mail\s+(?:é|foi)\s+(?:enviado|gerado)[^\n]{0,120}\n?',
    r'não\s+responda\s+(?:a\s+)?este[^\n]{0,60}\n?',
    r'mensagem\s+automática[^\n]{0,60}\n?',
    r'para\s+(?:maiores\s+)?informações[^\n]{0,80}\n?',
    r'\[?\s*imagem\s*\]?',
    r'_{5,}',
    r'-{5,}',
]
_RUIDO_RE = re.compile('|'.join(_RUIDO_PATTERNS), re.IGNORECASE)

# Mapa de tipo de ato → providência sugerida
_PROVIDENCIAS = {
    "intimação":    "Verificar prazo e providenciar manifestação/recurso cabível",
    "intimacao":    "Verificar prazo e providenciar manifestação/recurso cabível",
    "citação":      "Elaborar resposta à inicial (contestação) no prazo legal",
    "citacao":      "Elaborar resposta à inicial (contestação) no prazo legal",
    "audiência":    "Preparar pauta e documentos para a audiência",
    "audiencia":    "Preparar pauta e documentos para a audiência",
    "sentença":     "Analisar sentença e verificar cabimento de apelação (prazo: 15 dias úteis)",
    "sentenca":     "Analisar sentença e verificar cabimento de apelação (prazo: 15 dias úteis)",
    "acórdão":      "Analisar acórdão e verificar cabimento de REsp/RE/ED (prazo: 15 dias úteis)",
    "acordao":      "Analisar acórdão e verificar cabimento de REsp/RE/ED (prazo: 15 dias úteis)",
    "decisão":      "Analisar decisão e verificar cabimento de agravo/recurso cabível",
    "decisao":      "Analisar decisão e verificar cabimento de agravo/recurso cabível",
    "despacho":     "Cumprir determinação do despacho no prazo fixado",
    "embargos":     "Elaborar embargos de declaração (prazo: 5 dias úteis)",
    "recurso":      "Analisar e preparar contrarrazões no prazo legal",
    "contrarraz":   "Elaborar contrarrazões ao recurso interposto",
    "manifestação": "Elaborar manifestação no prazo fixado",
    "manifestacao": "Elaborar manifestação no prazo fixado",
    "petição":      "Atender à determinação — elaborar petição requerida",
    "peticao":      "Atender à determinação — elaborar petição requerida",
    "diligência":   "Cumprir diligência determinada no prazo fixado",
    "diligencia":   "Cumprir diligência determinada no prazo fixado",
}

def _limpar_corpo(corpo):
    """Remove ruído institucional e formata o texto da intimação."""
    texto = _RUIDO_RE.sub(' ', corpo)
    # Colapsa espaços múltiplos e linhas em branco excessivas
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    texto = re.sub(r'[ \t]{2,}', ' ', texto)
    return texto.strip()

def _extrair_partes(corpo):
    """Tenta extrair polo ativo e passivo da intimação, sem advogados."""
    padroes = [
        r'(?:autor[a]?|requerente|reclamante|impetrante|exequente|agravante|apelante)\s*[:\-]?\s+([A-ZÀ-Ú][A-ZÀ-Úa-zà-ú\s]{4,60})',
        r'(?:réu|ré|requerido[a]?|reclamado[a]?|impetrado[a]?|executado[a]?|agravado[a]?|apelado[a]?)\s*[:\-]?\s+([A-ZÀ-Ú][A-ZÀ-Úa-zà-ú\s]{4,60})',
    ]
    partes = []
    _CORTA_PARTE = re.compile(
        r'\s+(?:advogado[s]?|adv\.|oab|login|sc\d{4}|\(sc|x\s+execut|\d{7}-\d{2})',
        re.IGNORECASE
    )
    for pat in padroes:
        m = re.search(pat, corpo, re.IGNORECASE)
        if m:
            nome = m.group(1).strip()
            # Remove tudo a partir de "Advogado(s)", OAB, parênteses de código
            corte = _CORTA_PARTE.search(nome)
            if corte:
                nome = nome[:corte.start()].strip()
            if len(nome) > 3:
                partes.append(nome[:60])
    return partes

def _extrair_data_publicacao(corpo):
    """Extrai data de publicação/disponibilização do corpo."""
    padroes = [
        r'(?:publicad[ao]|disponibilizad[ao])\s+(?:em\s+)?(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4})',
        r'(?:data\s+da\s+(?:publicação|disponibilização))[:\s]+(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4})',
        r'(?:em\s+)(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',
    ]
    for pat in padroes:
        m = re.search(pat, corpo, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None

# ── Boilerplate que não é conteúdo do ato ─────────────────────────────
_BOILERPLATE = re.compile(
    r'(?:os\s+seguintes\s+processos\s+tiveram'
    r'|nova\s+(?:movimenta[çc][aã]o|intima[çc][aã]o)'
    r'|num\.\s*processo\b'
    r'|jornal\s+(?:di[aá]rio|eletr[oô]nico)'
    r'|org[ãa]o\s+julgador'
    r'|sua\s+conta\s+no\s+sistema'
    r'|login\s+\w+.*?confirma[çc][aã]o'
    r'|c[oó]digo\s+de\s+confirma[çc][aã]o'
    r'|detectamos\s+um\s+acesso'
    r'|advogado\s+de\s+origem'
    r'|c[oó]digo\s+da\s+publica[çc][aã]o'
    r'|sistema\s+eproc'
    r'|p[aá]gina\s+\d)',
    re.IGNORECASE
)

# Marcadores de início do conteúdo real do ato
_INICIO_ATO = re.compile(
    # Tipo de ato como palavra isolada (pode vir com espaços ao redor)
    r'\b(DECIS[ÃA]O(?:\s+INTERLOCUT[ÓO]RIA|\s+MONOCR[ÁA]TICA)?'
    r'|DESPACHO(?:\s+ORDIN[ÁA]T[ÓO]RIO)?'
    r'|SENTEN[ÇC]A(?:\s+(?:CONDENAT[ÓO]RIA|ABSOLUT[ÓO]RIA|HOMOLOGATÓRIA))?'
    r'|AC[ÓO]RD[ÃA]O'
    r'|EMBARGO[S]?\s+DE\s+DECLARA[ÇC][ÃA]O'
    r'|ATO\s+ORDIN[ÁA]T[ÓO]RIO'
    r')\b',
    re.IGNORECASE
)

# Abertura narrativa de uma decisão/sentença
_ABERTURA = re.compile(
    r'\b(?:vistos[,\s]|trata-se\s+de\s|cuida-se\s+de\s|examino\s+|em\s+an[aá]lise\s)',
    re.IGNORECASE
)

# Dispositivo/conclusão
_DISPOSITIVO = re.compile(
    r'\b(?:diante\s+do\s+exposto|ante\s+o\s+exposto|pelo\s+exposto|em\s+face\s+do\s+exposto)\b'
    r'|\b(?:defiro|indefiro|homologo|condeno|absolvo)\b'
    r'|\bjulgo\s+(?:procedente|improcedente|extinto|parcialmente)\b'
    r'|\b(?:determino|autorizo|indefiro)\s+\w'
    r'|\bprazo\s+de\s+\d+\s+(?:dias?|horas?)\b',
    re.IGNORECASE
)

def _extrair_teor_principal(corpo):
    """
    Extrai o conteúdo real do ato judicial intimado.
    Funciona tanto com texto plano quanto HTML já convertido.
    Retorna string com o teor ou None se só boilerplate.
    """
    if not corpo:
        return None

    # Estratégia 1: localiza o cabeçalho do tipo de ato (SENTENÇA, DECISÃO, etc.)
    # e extrai o bloco que vem depois
    m = _INICIO_ATO.search(corpo)
    if m:
        # Pega conteúdo a partir do cabeçalho
        trecho = corpo[m.start():m.start() + 700]
        trecho = re.sub(r'\s+', ' ', trecho).strip()
        # Verifica que não é só boilerplate
        if len(trecho) > 60 and not _BOILERPLATE.search(trecho[:80]):
            return trecho[:500]

    # Estratégia 2: abertura clássica (Vistos, Trata-se, etc.)
    m = _ABERTURA.search(corpo)
    if m:
        trecho = corpo[m.start():m.start() + 600]
        trecho = re.sub(r'\s+', ' ', trecho).strip()
        if len(trecho) > 60 and not _BOILERPLATE.search(trecho[:80]):
            return trecho[:500]

    # Estratégia 3: dispositivo/conclusão com contexto anterior
    m = _DISPOSITIVO.search(corpo)
    if m:
        inicio = max(0, m.start() - 150)
        fim    = min(len(corpo), m.end() + 350)
        trecho = re.sub(r'\s+', ' ', corpo[inicio:fim]).strip()
        if len(trecho) > 40 and not _BOILERPLATE.search(trecho[:80]):
            return trecho[:500]

    # Estratégia 4: maior bloco de texto que não é boilerplate
    # Divide em parágrafos (quebras duplas OU frases longas separadas por ponto)
    blocos = re.split(r'\n{2,}|\.\s{2,}', corpo)
    for bloco in sorted(blocos, key=len, reverse=True):
        bloco = re.sub(r'\s+', ' ', bloco.strip())
        if len(bloco) < 60:
            continue
        if _BOILERPLATE.search(bloco[:100]):
            continue
        # Descarta blocos que são só metadados
        if re.match(r'^(?:\d{7}-\d{2}|processo:|exequente\s|executado\s|apelante\s|advogado)', bloco, re.IGNORECASE):
            continue
        return bloco[:500]

    return None

def construir_compromisso(tipo_ato_raw, corpo_lower):
    """
    Retorna a AÇÃO a ser realizada — não metadados do e-mail.
    Ex: "Elaborar contestação", "Preparar para audiência", "Analisar sentença e verificar recurso"
    """
    # Mapa direto: keyword no corpo → ação concreta
    acoes = [
        # Citação → contestação
        (r'cita[çc][aã]o|citado|foi\s+citad[ao]',
         "Elaborar contestação no prazo legal"),
        # Audiência / sessão → preparar
        (r'audi[eê]ncia\s+(?:de\s+)?(?:instru[çc][aã]o|conci?lia[çc][aã]o|julgamento|custodia)',
         "Preparar para audiência"),
        (r'sess[aã]o\s+de\s+julgamento|pauta\s+de\s+julgamento',
         "Preparar para sessão de julgamento"),
        (r'audi[eê]ncia',
         "Preparar para audiência"),
        # Sentença → verificar apelação
        (r'senten[çc]a',
         "Analisar sentença e verificar cabimento de recurso (prazo: 15 dias úteis)"),
        # Acórdão → verificar REsp/RE/ED
        (r'ac[oó]rd[aã]o',
         "Analisar acórdão e verificar cabimento de REsp/RE/ED (prazo: 15 dias úteis)"),
        # Embargos de declaração
        (r'embargos\s+de\s+declara[çc][aã]o',
         "Elaborar embargos de declaração (prazo: 5 dias úteis)"),
        # Contrarrazões
        (r'contrarraz[õo]es|recurso\s+(?:da\s+)?(?:parte\s+)?(?:autora|adversa|contr[aá]ria)',
         "Elaborar contrarrazões ao recurso interposto (prazo: 15 dias úteis)"),
        # Agravo
        (r'agravo\s+(?:de\s+instrumento|regimental|interno)',
         "Elaborar resposta ao agravo"),
        # Manifestação / prazo genérico
        (r'manifeste[-\s]se|manifestar[-\s]se|manifestem[-\s]se',
         "Elaborar manifestação no prazo fixado"),
        # Diligência
        (r'dilig[eê]ncia',
         "Cumprir diligência no prazo fixado"),
        # Cumprimento de sentença / execução
        (r'cumprimento\s+de\s+senten[çc]a|execu[çc][aã]o',
         "Verificar cumprimento de sentença / providenciar defesa na execução"),
        # Perícia
        (r'per[ií]cia|perito',
         "Acompanhar perícia e verificar necessidade de assistente técnico"),
        # Despacho genérico
        (r'despacho',
         "Verificar determinação do despacho e cumprir no prazo"),
        # Decisão interlocutória
        (r'decis[aã]o\s+(?:interlocut[oó]ria|monocr[aá]tica)',
         "Analisar decisão e verificar cabimento de agravo de instrumento"),
        # Intimação genérica
        (r'intima[çc][aã]o|intimad[ao]',
         "Analisar intimação e adotar providência cabível no prazo"),
    ]

    for pattern, acao in acoes:
        if re.search(pattern, corpo_lower, re.IGNORECASE):
            return acao

    # Fallback pelo tipo_ato_raw
    fallbacks = {
        "citação":    "Elaborar contestação no prazo legal",
        "citacao":    "Elaborar contestação no prazo legal",
        "audiência":  "Preparar para audiência",
        "audiencia":  "Preparar para audiência",
        "sentença":   "Analisar sentença e verificar cabimento de recurso",
        "sentenca":   "Analisar sentença e verificar cabimento de recurso",
        "acórdão":    "Analisar acórdão e verificar REsp/RE/ED",
        "acordao":    "Analisar acórdão e verificar REsp/RE/ED",
        "embargos":   "Elaborar embargos de declaração",
        "recurso":    "Elaborar contrarrazões ao recurso",
        "prazo":      "Analisar intimação e adotar providência no prazo",
        "peticao":    "Elaborar petição determinada",
        "petição":    "Elaborar petição determinada",
        "diligencia": "Cumprir diligência no prazo",
        "diligência": "Cumprir diligência no prazo",
    }
    if tipo_ato_raw and tipo_ato_raw.lower() in fallbacks:
        return fallbacks[tipo_ato_raw.lower()]

    return "Verificar ato processual e adotar providência cabível"

def construir_resumo(tribunal, assunto, corpo, processo, data_email=None):
    """
    Retorna o conteúdo real do ato processual intimado:
    decisão interlocutória (deferida/indeferida), sentença
    (procedente/improcedente), despacho (o que determina),
    ato ordinatório (o que exige).
    SEM: processo, partes, tribunal, advogados, DJe, boilerplate.
    """
    # Usa o corpo bruto para encontrar o teor — o _RUIDO_RE pode cortar
    # trechos relevantes se aplicado antes
    teor = _extrair_teor_principal(corpo)
    return teor or ""

# ── Banco de dados — controle de duplicatas ──────────────────────────

def init_email_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS emails_processados (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id  TEXT UNIQUE,
            processado_em TEXT DEFAULT (datetime('now','localtime')),
            resultado   TEXT
        )
    """)
    conn.commit()
    conn.close()

def ja_processado(message_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.execute("SELECT id FROM emails_processados WHERE message_id=?", (message_id,))
    existe = cur.fetchone() is not None
    conn.close()
    return existe

def marcar_processado(message_id, resultado):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR IGNORE INTO emails_processados (message_id, resultado) VALUES (?,?)",
        (message_id, resultado)
    )
    conn.commit()
    conn.close()

# ── Envio para API ────────────────────────────────────────────────────

def enviar_prazo(data_prazo, cliente, compromisso, tipo, resumo, tribunal="", partes=""):
    """POST para /api/prazos."""
    payload = {
        "data_prazo":  data_prazo.isoformat() if hasattr(data_prazo, 'isoformat') else data_prazo,
        "cliente":     cliente,
        "compromisso": compromisso,
        "tipo":        tipo,
        "resumo":      resumo,
        "tribunal":    tribunal or "",
        "partes":      partes or "",
    }
    try:
        r = requests.post(f"{API_BASE}/api/prazos", json=payload, timeout=5)
        if r.status_code == 201:
            log.info(f"  ✓ Cadastrado: {cliente} — {compromisso} ({payload['data_prazo']})")
            return True
        else:
            log.warning(f"  ✗ API retornou {r.status_code}: {r.text}")
            return False
    except requests.exceptions.ConnectionError:
        log.error("  ✗ Não foi possível conectar ao servidor de prazos (localhost:5001). Está rodando?")
        return False

# ── Processamento de e-mail ───────────────────────────────────────────

def processar_email(msg):
    """Processa uma mensagem e retorna dict com os dados extraídos, ou None."""
    assunto  = decode_header_value(msg.get("Subject", ""))
    remetente = decode_header_value(msg.get("From", ""))
    date_str = msg.get("Date", "")
    msg_id   = msg.get("Message-ID", "").strip()

    # Data do e-mail
    try:
        data_email = parsedate_to_datetime(date_str).date()
    except Exception:
        data_email = date.today()

    corpo = get_email_body(msg)
    texto_completo = f"{assunto} {corpo}"
    texto_lower    = texto_completo.lower()

    # Identifica tribunal
    tribunal = identificar_tribunal(remetente, assunto, corpo)
    if not tribunal:
        return None  # não é e-mail de tribunal

    # Extrai dados
    processo   = extrair_processo(texto_completo)
    tipo, data_prazo = extrair_tipo_e_prazo(texto_lower, data_email)
    cliente    = extrair_nome_cliente(assunto, corpo, processo)

    # Identifica tipo de ato para o texto do compromisso
    tipo_ato_raw = None
    for kw in TIPOS_ATO:
        if kw in texto_lower:
            tipo_ato_raw = kw
            break

    compromisso = construir_compromisso(tipo_ato_raw, texto_lower)
    resumo      = construir_resumo(tribunal, assunto, corpo, processo, data_email)
    partes_list = _extrair_partes(corpo)
    partes      = " × ".join(partes_list) if partes_list else ""

    return {
        "msg_id":     msg_id,
        "tribunal":   tribunal,
        "partes":     partes,
        "data_prazo": data_prazo,
        "cliente":    cliente,
        "compromisso": compromisso,
        "tipo":       tipo,
        "resumo":     resumo,
    }

# ── IMAP ─────────────────────────────────────────────────────────────

def conectar_imap(cfg):
    """Conecta ao servidor IMAP e retorna conexão autenticada."""
    servidor = cfg["imap_server"]
    porta    = cfg.get("imap_port", 993)
    usuario  = cfg["email"]
    senha    = cfg["senha"]

    log.info(f"Conectando a {servidor}:{porta} ({usuario})...")
    mail = imaplib.IMAP4_SSL(servidor, porta)
    mail.login(usuario, senha)
    log.info("Conectado com sucesso.")
    return mail

def buscar_emails_tribunal(mail, cfg):
    """Busca e-mails não lidos de domínios .jus.br."""
    mail.select("INBOX")
    apenas_nao_lidos = cfg.get("apenas_nao_lidos", True)

    criterios = []
    if apenas_nao_lidos:
        criterios.append("UNSEEN")

    # Busca por domínio genérico .jus.br
    criterios.append('FROM "@*.jus.br"')

    # Também busca por e-mails encaminhados
    criterio_principal = " ".join(criterios)

    ids_encontrados = set()
    _, data = mail.search(None, criterio_principal)
    for uid in (data[0] or b"").split():
        ids_encontrados.add(uid)

    # Busca adicional por assunto (para e-mails encaminhados)
    for kw in ["intimação", "prazo processual", "citação", "audiência",
               "e-proc", "pje", "projudi"]:
        try:
            _, data = mail.search(None, f'SUBJECT "{kw}"')
            for uid in (data[0] or b"").split():
                ids_encontrados.add(uid)
        except Exception:
            pass

    return list(ids_encontrados)

def sincronizar(cfg, limite=50):
    """Sincroniza e-mails de tribunais com o sistema de prazos."""
    init_email_db()
    novos = 0
    ignorados = 0
    erros = 0

    try:
        mail = conectar_imap(cfg)
    except Exception as e:
        log.error(f"Falha na conexão IMAP: {e}")
        return {"novos": 0, "ignorados": 0, "erros": 1, "msg": str(e)}

    try:
        uids = buscar_emails_tribunal(mail, cfg)
        log.info(f"Encontrados {len(uids)} e-mails candidatos.")

        for uid in uids[-limite:]:  # processa os mais recentes primeiro
            try:
                _, msg_data = mail.fetch(uid, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                msg_id = msg.get("Message-ID", f"uid-{uid.decode()}").strip()

                if ja_processado(msg_id):
                    ignorados += 1
                    continue

                dados = processar_email(msg)
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
                log.error(f"Erro ao processar UID {uid}: {e}")
                erros += 1

        mail.logout()

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

# ── Modo daemon (loop contínuo) ───────────────────────────────────────

def rodar_daemon(cfg):
    intervalo = cfg.get("intervalo_minutos", 30) * 60
    log.info(f"Iniciando modo daemon — verificando e-mails a cada {cfg.get('intervalo_minutos',30)} min.")
    while True:
        try:
            sincronizar(cfg)
        except Exception as e:
            log.error(f"Erro no daemon: {e}")
        log.info(f"Aguardando {cfg.get('intervalo_minutos',30)} minutos...")
        time.sleep(intervalo)

# ── Main ─────────────────────────────────────────────────────────────

def carregar_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"\n⚠  Arquivo de configuração não encontrado: {CONFIG_FILE}")
        print("   Execute primeiro: python configurar_email.py\n")
        sys.exit(1)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    cfg = carregar_config()
    modo = sys.argv[1] if len(sys.argv) > 1 else "sync"

    if modo == "daemon":
        rodar_daemon(cfg)
    else:
        resultado = sincronizar(cfg)
        print(f"\n{resultado['msg']}")
