"""
Workflows PDF v2 — Redesign completo com validadores + visual premium
Flowcharts com canvas drawing, sombras, setas reais, nodes arredondados
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Frame, PageTemplate, Flowable
)
from reportlab.platypus.doctemplate import BaseDocTemplate, NextPageTemplate
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group
from reportlab.graphics import renderPDF
import os, math

W, H = A4

# ═══════════════════════════════════════════
# PALETA REFINADA
# ═══════════════════════════════════════════
NAVY       = HexColor("#0D1B2A")
NAVY_MED   = HexColor("#1B2A4A")
NAVY_LIGHT = HexColor("#2B3D5B")
GOLD       = HexColor("#C9A84C")
GOLD_LIGHT = HexColor("#E8D5A3")
GOLD_PALE  = HexColor("#F5EDD6")
BG_PAGE    = HexColor("#FAFAF8")
BG_CARD    = HexColor("#FFFFFF")
BG_ALT     = HexColor("#F7F6F3")
BORDER     = HexColor("#E2E0DB")
TEXT_DARK   = HexColor("#1A1A1A")
TEXT_MED    = HexColor("#4A4A4A")
TEXT_LIGHT  = HexColor("#8A8A8A")
TEXT_MUTED  = HexColor("#B0B0B0")

# Node colors
NODE_TRIGGER   = HexColor("#1B7A3D")
NODE_OPUS      = HexColor("#1B2A4A")
NODE_SONNET    = HexColor("#2E5984")
NODE_SCRIPT    = HexColor("#5B4A8A")
NODE_VALIDATE  = HexColor("#B8860B")
NODE_OUTPUT    = HexColor("#8B2500")
NODE_GATE      = HexColor("#C0392B")

# Lighter versions for fills
FILL_TRIGGER   = HexColor("#E8F5EC")
FILL_OPUS      = HexColor("#E3E8F0")
FILL_SONNET    = HexColor("#E8EEF5")
FILL_SCRIPT    = HexColor("#EDEAF3")
FILL_VALIDATE  = HexColor("#FFF5D6")
FILL_OUTPUT    = HexColor("#FDE8E0")
FILL_GATE      = HexColor("#FDEDED")

OUTPUT_PATH = r"C:\Users\Rodrigo\Desktop\analise_critica_moukarzel\07_workflows_mapeamento_v2.pdf"


# ═══════════════════════════════════════════
# ESTILOS
# ═══════════════════════════════════════════

def ps(name, **kw):
    defaults = {
        'body': dict(fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=6),
        'h1': dict(fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=NAVY, spaceAfter=4, spaceBefore=0),
        'h2': dict(fontName='Helvetica-Bold', fontSize=15, leading=20, textColor=NAVY, spaceAfter=6, spaceBefore=14),
        'h3': dict(fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=NAVY_MED, spaceAfter=4, spaceBefore=8),
        'meta': dict(fontName='Helvetica', fontSize=9, leading=13, textColor=TEXT_LIGHT, spaceAfter=3),
        'bullet': dict(fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK, leftIndent=20, bulletIndent=8, spaceAfter=2),
        'small': dict(fontName='Helvetica', fontSize=8, leading=11, textColor=TEXT_MUTED, alignment=TA_CENTER),
        'note': dict(fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=TEXT_MED, spaceAfter=4),
    }
    params = defaults.get(name, defaults['body']).copy()
    params.update(kw)
    return ParagraphStyle(f'{name}_{id(kw)}', **params)


# ═══════════════════════════════════════════
# FLOWCHART FLOWABLE (Custom Drawing)
# ═══════════════════════════════════════════

class FlowChart(Flowable):
    """Flowchart profissional com nodes arredondados, setas e cores"""

    def __init__(self, steps, width=16*cm, node_height=28, spacing=6):
        Flowable.__init__(self)
        self.steps = steps
        self.chart_width = width
        self.node_h = node_height
        self.spacing = spacing
        self.arrow_h = 12
        # Calcular altura total
        n = len(steps)
        self.height = n * self.node_h + (n-1) * (self.spacing + self.arrow_h) + 10
        self.width = width

    def draw(self):
        c = self.canv
        y = self.height - 5

        for i, step in enumerate(self.steps):
            label = step.get('label', '')
            text = step.get('text', '')
            output = step.get('output', '')
            node_type = step.get('type', 'script')  # trigger, opus, sonnet, script, validate, output, gate
            parallel = step.get('parallel', False)

            # Cores por tipo
            colors = {
                'trigger':  (NODE_TRIGGER, FILL_TRIGGER, HexColor("#1B7A3D")),
                'opus':     (NODE_OPUS, FILL_OPUS, HexColor("#1B2A4A")),
                'sonnet':   (NODE_SONNET, FILL_SONNET, HexColor("#2E5984")),
                'script':   (NODE_SCRIPT, FILL_SCRIPT, HexColor("#5B4A8A")),
                'validate': (NODE_VALIDATE, FILL_VALIDATE, HexColor("#B8860B")),
                'output':   (NODE_OUTPUT, FILL_OUTPUT, HexColor("#8B2500")),
                'gate':     (NODE_GATE, FILL_GATE, HexColor("#C0392B")),
            }
            border_c, fill_c, label_c = colors.get(node_type, colors['script'])

            nh = self.node_h
            nw = self.chart_width

            # Sombra suave
            c.setFillColor(HexColor("#E8E8E8"))
            c.roundRect(2, y - nh - 1, nw, nh, 5, fill=1, stroke=0)

            # Node principal
            c.setFillColor(fill_c)
            c.setStrokeColor(border_c)
            c.setLineWidth(1.2)
            c.roundRect(0, y - nh, nw, nh, 5, fill=1, stroke=1)

            # Barra lateral colorida (accent)
            c.setFillColor(border_c)
            # Usar rect simples para a barra esquerda
            c.rect(0, y - nh + 2, 4, nh - 4, fill=1, stroke=0)

            # Marcador paralelo
            if parallel:
                c.setFillColor(GOLD)
                c.roundRect(nw - 55, y - 10, 50, 10, 2, fill=1, stroke=0)
                c.setFillColor(white)
                c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(nw - 30, y - 8.5, "PARALELO")

            # Label (tipo do step)
            c.setFillColor(label_c)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(12, y - 11, label.upper())

            # Texto principal
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica", 8.5)
            # Truncar se necessario
            max_chars = 85
            display_text = text[:max_chars] + ('...' if len(text) > max_chars else '')
            c.drawString(12, y - 23, display_text)

            # Output (lado direito)
            if output:
                c.setFillColor(TEXT_LIGHT)
                c.setFont("Courier", 7)
                c.drawRightString(nw - 8, y - 23, output)

            # Seta para proximo
            y -= nh

            if i < len(self.steps) - 1:
                arrow_x = nw / 2
                arrow_top = y - 2
                arrow_bot = y - self.arrow_h + 2

                c.setStrokeColor(GOLD)
                c.setLineWidth(1.5)
                c.line(arrow_x, arrow_top, arrow_x, arrow_bot)

                # Ponta da seta
                c.setFillColor(GOLD)
                c.setStrokeColor(GOLD)
                path = c.beginPath()
                path.moveTo(arrow_x - 4, arrow_bot + 3)
                path.lineTo(arrow_x, arrow_bot - 1)
                path.lineTo(arrow_x + 4, arrow_bot + 3)
                path.close()
                c.drawPath(path, fill=1, stroke=0)

                y -= (self.spacing + self.arrow_h)


# ═══════════════════════════════════════════
# TEMPLATE
# ═══════════════════════════════════════════

class DocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        f = Frame(2.2*cm, 2.2*cm, W - 4.4*cm, H - 4.4*cm, id='c')
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[f], onPage=self._cover),
            PageTemplate(id='content', frames=[f], onPage=self._content),
        ])

    def _cover(self, c, doc):
        c.saveState()
        # Fundo
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Faixa dourada lateral
        c.setFillColor(GOLD)
        c.rect(0, 0, 6*mm, H, fill=1, stroke=0)

        # Linhas decorativas sutis
        c.setStrokeColor(HexColor("#1A2744"))
        c.setLineWidth(0.2)
        for i in range(0, int(W), 50):
            c.line(i, 0, i, H)

        # Bloco dourado decorativo superior
        c.setFillColor(GOLD)
        c.rect(2*cm, H - 3.5*cm, 3*cm, 2*mm, fill=1, stroke=0)

        # Bloco dourado decorativo inferior
        c.rect(2*cm, 4.5*cm, W - 4*cm, 0.5*mm, fill=1, stroke=0)
        c.restoreState()

    def _content(self, c, doc):
        c.saveState()
        # Fundo sutil
        c.setFillColor(BG_PAGE)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Header line
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6)
        c.line(2.2*cm, H - 1.6*cm, W - 2.2*cm, H - 1.6*cm)

        c.setFillColor(TEXT_MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(2.2*cm, H - 1.35*cm, "MAPEAMENTO DE WORKFLOWS")
        c.drawRightString(W - 2.2*cm, H - 1.35*cm, "GASTAO DA ROSA & MOUKARZEL")

        # Footer
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(2.2*cm, 1.8*cm, W - 2.2*cm, 1.8*cm)

        pn = doc.page - 1
        c.setFont("Helvetica", 7.5)
        c.setFillColor(TEXT_MUTED)
        c.drawCentredString(W/2, 1.3*cm, f"{pn}")

        # Accent bar esquerda
        c.setFillColor(GOLD)
        c.rect(0, 1.8*cm, 2.5*mm, H - 3.6*cm, fill=1, stroke=0)
        c.restoreState()


# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

def gold_hr():
    return HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceBefore=8, spaceAfter=8)

def thin_hr():
    return HRFlowable(width="100%", thickness=0.3, color=BORDER, spaceBefore=4, spaceAfter=4)

def section_header(num, title):
    data = [[
        Paragraph(f'<font color="white" size="16"><b>{num}</b></font>',
                  ParagraphStyle('sn', alignment=TA_CENTER, fontName='Helvetica-Bold', leading=20)),
        Paragraph(f'<font color="{NAVY.hexval()}" size="14"><b>{title}</b></font>',
                  ParagraphStyle('st', fontName='Helvetica-Bold', leading=20))
    ]]
    t = Table(data, colWidths=[1.3*cm, 15*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), NAVY),
        ('BACKGROUND', (1,0),(1,0), GOLD_PALE),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0),(0,0), 'CENTER'),
        ('LEFTPADDING', (1,0),(1,0), 10),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LINEBELOW', (0,0),(-1,0), 1.5, GOLD),
    ]))
    return t

def info_card(items, bg=BG_ALT):
    """Card com informacoes key-value"""
    rows = []
    for key, val in items:
        rows.append([
            Paragraph(f'<b>{key}</b>', ParagraphStyle('ik', fontName='Helvetica-Bold', fontSize=8.5, textColor=TEXT_MED, leading=12)),
            Paragraph(val, ParagraphStyle('iv', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK, leading=12)),
        ])
    t = Table(rows, colWidths=[3.5*cm, 12.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), bg),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING', (0,0),(-1,-1), 8),
        ('LINEBELOW', (0,0),(-1,-2), 0.3, BORDER),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    return t

def make_table(headers, rows, col_widths=None):
    sh = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=11, alignment=TA_CENTER)
    sc = ParagraphStyle('tc', fontName='Helvetica', fontSize=8.5, textColor=TEXT_DARK, leading=11)
    scc = ParagraphStyle('tcc', fontName='Helvetica', fontSize=8.5, textColor=TEXT_DARK, leading=11, alignment=TA_CENTER)

    data = [[Paragraph(h, sh) for h in headers]]
    for row in rows:
        cells = [Paragraph(str(c), scc if (len(str(c)) < 20 and i > 0) else sc) for i, c in enumerate(row)]
        data.append(cells)

    if not col_widths:
        col_widths = [16.3*cm / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('BACKGROUND', (0,0),(-1,0), NAVY),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
        ('GRID', (0,0),(-1,-1), 0.3, BORDER),
        ('LINEBELOW', (0,0),(-1,0), 1, GOLD),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0,i),(-1,i), BG_ALT))
    t.setStyle(TableStyle(cmds))
    return t

def highlight_box(text, accent=GOLD):
    s = ParagraphStyle('hb', fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK)
    data = [[Paragraph(text, s)]]
    t = Table(data, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), GOLD_PALE),
        ('LEFTPADDING', (0,0),(-1,-1), 12),
        ('RIGHTPADDING', (0,0),(-1,-1), 12),
        ('TOPPADDING', (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LINEBELOW', (0,0),(-1,-1), 1.5, accent),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    return t


# ═══════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════

def build():
    doc = DocTemplate(OUTPUT_PATH, pagesize=A4,
                      topMargin=2.2*cm, bottomMargin=2.2*cm,
                      leftMargin=2.2*cm, rightMargin=2.2*cm)
    story = []

    # ═══ CAPA ═══
    story.append(Spacer(1, 4.5*cm))
    story.append(Paragraph('<font color="#C9A84C" size="10">DOCUMENTO 07  |  ANALISE CRITICA</font>',
                           ps('small', textColor=GOLD, fontSize=10)))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('Mapeamento<br/>de Workflows',
                           ps('h1', fontSize=34, leading=40, textColor=white)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('Diagramas dos 10 Workflows Atuais<br/>+ 10 Workflows Sugeridos com Validadores',
                           ps('body', fontSize=14, leading=20, textColor=GOLD_LIGHT)))
    story.append(Spacer(1, 3*cm))
    story.append(HRFlowable(width="50%", thickness=0.8, color=GOLD, spaceBefore=0, spaceAfter=16))
    story.append(Paragraph(
        'Sistema de Workflow Juridico v2.0<br/>'
        'Escritorio Gastao da Rosa &amp; Moukarzel<br/>'
        'Dr. Paulo Ekke Moukarzel Junior  |  OAB/SC',
        ps('body', fontSize=11, leading=16, textColor=HexColor("#BBBBBB"))))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph('Abril 2026  |  Confidencial',
                           ps('small', fontSize=9, textColor=HexColor("#778899"))))

    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # ═══ LEGENDA ═══
    story.append(Paragraph('Legenda dos Diagramas', ps('h2')))
    story.append(thin_hr())

    legend_items = [
        ('TRIGGER', 'Ponto de entrada / comando que inicia o workflow', NODE_TRIGGER, FILL_TRIGGER),
        ('OPUS 4-6', 'Agente Claude Opus — raciocinio profundo, redacao, auditoria', NODE_OPUS, FILL_OPUS),
        ('SONNET 4-6', 'Agente Claude Sonnet — pesquisa, revisao, verificacao', NODE_SONNET, FILL_SONNET),
        ('SCRIPT', 'Processamento via script Python ou ferramenta externa', NODE_SCRIPT, FILL_SCRIPT),
        ('VALIDADOR', 'Etapa de validacao/verificacao de qualidade (OBRIGATORIA)', NODE_VALIDATE, FILL_VALIDATE),
        ('OUTPUT', 'Resultado final entregue ao advogado', NODE_OUTPUT, FILL_OUTPUT),
        ('GATE HUMANO', 'Ponto de decisao que exige aprovacao humana antes de prosseguir', NODE_GATE, FILL_GATE),
    ]

    for label, desc, border_c, fill_c in legend_items:
        row = [[
            Paragraph(f'<b>{label}</b>',
                      ParagraphStyle(f'l{label}', fontName='Helvetica-Bold', fontSize=8,
                                     textColor=white if border_c in [NODE_TRIGGER, NODE_OPUS, NODE_SONNET, NODE_SCRIPT, NODE_GATE, NODE_OUTPUT] else TEXT_DARK,
                                     alignment=TA_CENTER, leading=11)),
            Paragraph(desc, ParagraphStyle(f'd{label}', fontName='Helvetica', fontSize=8.5, textColor=TEXT_DARK, leading=12)),
        ]]
        lt = Table(row, colWidths=[3*cm, 13.3*cm])
        lt.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), border_c),
            ('BACKGROUND', (1,0),(1,0), fill_c),
            ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0),(-1,-1), 5),
            ('BOTTOMPADDING', (0,0),(-1,-1), 5),
            ('LEFTPADDING', (0,0),(-1,-1), 6),
            ('ROUNDEDCORNERS', [3,3,3,3]),
        ]))
        story.append(lt)
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Principio fundamental:</b> Todo workflow inclui pelo menos uma etapa de <b>VALIDACAO</b> '
        'antes de produzir output final. Nenhum conteudo e entregue sem verificacao.',
        ps('body', textColor=NODE_VALIDATE)
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════
    # PARTE I — 10 WORKFLOWS ATUAIS
    # ═══════════════════════════════════════

    story.append(Paragraph('<font color="#C9A84C">PARTE I</font>', ps('small', fontSize=11, textColor=GOLD)))
    story.append(Paragraph('Workflows Atuais', ps('h1')))
    story.append(gold_hr())

    # ──── 1. paulo-estilo-juridico ────
    story.append(section_header('1', 'Skill: paulo-estilo-juridico'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Motor de redacao juridica no estilo do Dr. Paulo Moukarzel — 5 etapas', ps('meta')))

    story.append(FlowChart([
        {'label': 'Trigger', 'text': 'Coletar informacoes — nome, tipo de peca, tribunal, processo, documentos, bases legais', 'type': 'trigger', 'output': 'Dados do caso'},
        {'label': 'Etapa 2 — Consulta', 'text': 'Buscar pecas _vf do mesmo tipo em indice_vf.json para replicar estrutura argumentativa', 'type': 'script', 'output': 'indice_vf.json'},
        {'label': 'Etapa 3 — Estilo', 'text': 'Ler perfil-estilo.md (conectivos, formulas, padroes extraidos de 292 pecas reais)', 'type': 'script', 'output': 'perfil-estilo.md'},
        {'label': 'Etapa 4 — Redacao [Opus]', 'text': 'Redigir aplicando 13 principios obrigatorios: fontes primarias, cadeia documental, precisao', 'type': 'opus', 'output': 'Texto da peca'},
        {'label': 'Etapa 5 — Geracao', 'text': 'gerar_peticao.py: Arial 12pt, espacamento 1.5, margens juridicas 3cm/2cm, timbre automatico', 'type': 'script', 'output': '.docx final'},
    ]))

    story.append(PageBreak())

    # ──── 2. criar-agentes ────
    story.append(section_header('2', 'Skill: criar-agentes'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Criar agentes especializados seguindo padroes Anthropic — 4 etapas', ps('meta')))

    story.append(FlowChart([
        {'label': 'Etapa 1 — Escopo', 'text': 'Entender: o que faz, o que nao faz, quem invoca, ferramentas disponiveis', 'type': 'trigger', 'output': 'Requisitos'},
        {'label': 'Etapa 2 — Referencia', 'text': 'Consultar catalogo de ferramentas e padroes Anthropic de agent design', 'type': 'script', 'output': 'Ref tools'},
        {'label': 'Etapa 3 — Rascunho [Opus]', 'text': 'Rascunhar .md com frontmatter YAML + responsabilidades + processo + formato', 'type': 'opus', 'output': 'Rascunho .md'},
        {'label': 'Etapa 4 — Revisao', 'text': 'Validar contra checklist de qualidade e salvar em .claude/agents/', 'type': 'script', 'output': '.claude/agents/*.md'},
    ]))

    story.append(Spacer(1, 0.5*cm))

    # ──── 3. /novo-caso ────
    story.append(section_header('3', 'Command: /novo-caso'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Criar caso novo com estrutura completa de pastas — 5 etapas', ps('meta')))

    story.append(FlowChart([
        {'label': 'Etapa 1 — Coleta', 'text': 'Coletar: nome MAIUSCULO, processo CNJ, vara, polo, parte adversa, prazo fatal', 'type': 'trigger', 'output': 'Dados brutos'},
        {'label': 'Etapa 2 — Confirmacao', 'text': 'Exibir resumo e aguardar confirmacao do usuario antes de criar qualquer arquivo', 'type': 'gate', 'output': 'OK / Cancelar'},
        {'label': 'Etapa 3 — Estrutura', 'text': 'Criar pastas: Clientes/<CLIENTE>/pipeline/ + output_claude/', 'type': 'script', 'output': 'Diretorios'},
        {'label': 'Etapa 4 — caso.json', 'text': 'Gerar caso.json com metadados completos e pipeline vazio', 'type': 'script', 'output': 'caso.json'},
        {'label': 'Etapa 5 — Feedback', 'text': 'Exibir confirmacao do caso criado + proximos passos sugeridos ao usuario', 'type': 'output', 'output': 'Resumo'},
    ]))

    story.append(PageBreak())

    # ──── 4. /caso (hub) ────
    story.append(section_header('4', 'Command: /caso (Hub de 8 Sub-Comandos)'))
    story.append(Spacer(1, 0.3*cm))

    story.append(make_table(
        ['Sub-comando', 'Tipo', 'Descricao'],
        [
            ['/caso status', 'CONSULTA', 'Status detalhado — le caso.json, calcula dias ate prazo'],
            ['/caso listar', 'CONSULTA', 'Painel de todos os casos ativos do escritorio'],
            ['/caso prazos', 'CONSULTA', 'Casos ordenados: VENCIDO > URGENTE > OK > CONCLUIDO'],
            ['/caso contestacao', 'PIPELINE', 'Dispara pipeline completo de contestacao (5 etapas)'],
            ['/caso recurso', 'PIPELINE', 'Dispara pipeline de recursos REsp/RE (4 etapas)'],
            ['/caso placeholders', 'CONSULTA', 'Lista [PLACEHOLDER] pendentes via placeholder_scan.py'],
            ['/caso indexar', 'MANUTENCAO', 'Atualiza indice de arquivos _vf via indexar_vf.py'],
        ],
        col_widths=[3.5*cm, 2.5*cm, 10.3*cm]
    ))

    story.append(Spacer(1, 0.5*cm))

    # ──── 5. /doit_like_me ────
    story.append(section_header('5', 'Command: /doit_like_me'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Atalho rapido — ativa a skill paulo-estilo-juridico imediatamente, sem etapas intermediarias.', ps('body')))

    story.append(FlowChart([
        {'label': 'Trigger: /doit_like_me', 'text': 'Usuario invoca comando de atalho', 'type': 'trigger', 'output': ''},
        {'label': 'Ativacao Direta', 'text': 'Carrega skill paulo-estilo-juridico e inicia workflow de redacao completo', 'type': 'opus', 'output': 'Skill ativa'},
    ], node_height=26, spacing=4))

    story.append(PageBreak())

    # ──── 6. Pipeline Contestacao ────
    story.append(section_header('6', 'Pipeline: Contestacao (5 Etapas)'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Orquestrador: Sonnet | 15 agentes disponiveis, ~7 executados por run', ps('meta')))

    story.append(FlowChart([
        {'label': 'Trigger', 'text': '/caso contestacao <cliente> — Orquestrador Sonnet inicia pipeline', 'type': 'trigger', 'output': 'caso.json'},
        {'label': 'Etapa 1a — Analista [Opus]', 'text': 'Le documentos, extrai fatos, argumentos adversos, dispositivos legais, cronologia', 'type': 'opus', 'output': 'analysis_*.txt', 'parallel': True},
        {'label': 'Etapa 1b — Pesq. Magistrado [Sonnet]', 'text': 'Padrao decisorio do juiz, tendencias, sensibilidades, precedentes', 'type': 'sonnet', 'output': 'perfil_mag_*.txt', 'parallel': True},
        {'label': 'Etapa 2 — Redator [Opus]', 'text': 'Recebe analise + perfil magistrado. Redige no estilo Paulo com 13 principios', 'type': 'opus', 'output': 'contest_*_v1.txt'},
        {'label': 'Etapa 3a — Rev. Juridico [Sonnet]', 'text': 'Cobertura de teses, artigos, jurisprudencia, cadeia documental (doc. X)', 'type': 'sonnet', 'output': 'review_jur_*.txt', 'parallel': True},
        {'label': 'Etapa 3b — Rev. Linguistico [Sonnet]', 'text': 'Aderencia ao estilo: vocabulario, conectivos, sem "Trata-se", sem "v. acordao"', 'type': 'sonnet', 'output': 'review_ling_*.txt', 'parallel': True},
        {'label': 'Etapa 4 — Auditor Final [Opus]', 'text': 'Consolida v1 + dois relatorios de revisao. Aplica correcoes coerentes', 'type': 'opus', 'output': 'contest_*_final.txt'},
        {'label': 'Etapa 5 — Gerador .docx [Sonnet]', 'text': 'gerar_peticao.py: timbre, Arial 12pt, margens juridicas, numeracao', 'type': 'script', 'output': 'CONTESTACAO_*.docx'},
    ]))

    story.append(PageBreak())

    # ──── 7. Pipeline Recursos ────
    story.append(section_header('7', 'Pipeline: Recursos REsp / RE (4 Etapas)'))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Orquestrador: Opus | Gera dois documentos independentes simultaneamente', ps('meta')))

    story.append(FlowChart([
        {'label': 'Trigger', 'text': '/caso recurso <cliente> — Orquestrador Opus inicia pipeline', 'type': 'trigger', 'output': 'caso.json'},
        {'label': 'Etapa 1a — Pesq. Jurisp. [Sonnet]', 'text': 'Jurisprudencia autenticada STJ/STF com numero, relator, data, ementa', 'type': 'sonnet', 'output': 'jurisp_*.txt', 'parallel': True},
        {'label': 'Etapa 1b — Redator REsp [Opus]', 'text': 'Acordao como sujeito, violacao como predicado. Prequestionamento explicito', 'type': 'opus', 'output': 'resp_*.txt', 'parallel': True},
        {'label': 'Etapa 1c — Redator RE [Opus]', 'text': 'Repercussao geral, violacao direta CF. Teses subsidiarias incluidas', 'type': 'opus', 'output': 're_*.txt', 'parallel': True},
        {'label': 'Etapa 2a — Rev. Prequestion. [Sonnet]', 'text': 'Todos os dispositivos foram debatidos no acordao recorrido?', 'type': 'sonnet', 'output': 'review_preq.txt', 'parallel': True},
        {'label': 'Etapa 2b — Rev. Estilo [Sonnet]', 'text': 'Conectivos do corpus, abertura de secoes, sem alineas a/b/c no corpo', 'type': 'sonnet', 'output': 'review_estilo.txt', 'parallel': True},
        {'label': 'Etapa 3 — Auditor Final [Opus]', 'text': 'Consolida correcoes de prequestionamento + estilo em ambos os recursos', 'type': 'opus', 'output': '*_final.txt'},
        {'label': 'Etapa 4 — Gerador .docx [Sonnet]', 'text': 'Dois documentos .docx independentes: REsp + RE com formatacao oficial', 'type': 'script', 'output': '2x .docx'},
    ]))

    story.append(PageBreak())

    # ──── 8-10. Scripts ────
    story.append(section_header('8', 'Script: gerar_peticao.py'))
    story.append(Spacer(1, 0.2*cm))
    story.append(FlowChart([
        {'label': 'Input', 'text': 'Parametros: --titulo, --cliente, --conteudo, --cidade, --advogado, --oab', 'type': 'trigger', 'output': 'Args CLI'},
        {'label': 'Carregar Template', 'text': 'Template .dotx com identidade visual do escritorio (timbre, fontes, margens)', 'type': 'script', 'output': '.dotx'},
        {'label': 'Formatar', 'text': 'Classificar paragrafos e aplicar: Arial 12pt, espacamento 1.5, margens 3cm/2cm', 'type': 'script', 'output': 'Formatado'},
        {'label': 'Output', 'text': 'Salvar em output_claude/ com nome padronizado TIPO_CLIENTE_DATA.docx', 'type': 'output', 'output': '.docx'},
    ], node_height=26))

    story.append(Spacer(1, 0.4*cm))
    story.append(section_header('9', 'Script: indexar_vf.py'))
    story.append(Spacer(1, 0.2*cm))
    story.append(FlowChart([
        {'label': 'Escanear', 'text': 'Varrer diretorios de Clientes/ buscando sufixo _vf.docx', 'type': 'trigger', 'output': 'Pastas'},
        {'label': 'Classificar', 'text': 'Organizar por tipo: REsp, RE, HC, Contestacao, Apelacao, etc.', 'type': 'script', 'output': 'Tipos'},
        {'label': 'Output', 'text': 'Gerar data/indice_vf.json com 668+ arquivos indexados', 'type': 'output', 'output': 'indice_vf.json'},
    ], node_height=26))

    story.append(Spacer(1, 0.4*cm))
    story.append(section_header('10', 'Script: placeholder_scan.py'))
    story.append(Spacer(1, 0.2*cm))
    story.append(FlowChart([
        {'label': 'Escanear', 'text': 'Buscar pastas pipeline/ de todos os casos ativos', 'type': 'trigger', 'output': 'Pastas'},
        {'label': 'Detectar', 'text': 'Escanear .txt e .docx por padroes [PLACEHOLDER] e [VERIFICAR]', 'type': 'script', 'output': 'Matches'},
        {'label': 'Output', 'text': 'Gerar data/placeholders.json com relatorio por caso', 'type': 'output', 'output': 'placeholders.json'},
    ], node_height=26))

    story.append(PageBreak())

    # ═══════════════════════════════════════
    # PARTE II — 10 WORKFLOWS SUGERIDOS
    # ═══════════════════════════════════════

    story.append(Paragraph('<font color="#C9A84C">PARTE II</font>', ps('small', fontSize=11, textColor=GOLD)))
    story.append(Paragraph('10 Workflows Sugeridos', ps('h1')))
    story.append(gold_hr())

    story.append(highlight_box(
        '<b>Principio de design:</b> Todo workflow sugerido inclui etapa(s) de <font color="#B8860B"><b>VALIDACAO</b></font> '
        'obrigatoria(s) antes de entregar qualquer output. Nenhum conteudo gerado por IA sai do sistema sem ser verificado. '
        'Workflows criticos incluem <font color="#C0392B"><b>GATE HUMANO</b></font> que bloqueia '
        'a geracao final ate aprovacao do advogado.'
    ))
    story.append(Spacer(1, 0.3*cm))

    # Tabela resumo
    story.append(make_table(
        ['#', 'Workflow', 'Tipo', 'Prioridade', 'Esforco'],
        [
            ['1', 'Gestao de Prazos', 'Cmd + Cron', 'CRITICO', '3-5 dias'],
            ['2', 'Pesquisa Jurisprudencial', 'Command', 'QUICK WIN', '2-3 dias'],
            ['3', 'Embargos de Declaracao', 'Pipeline', 'QUICK WIN', '5-7 dias'],
            ['4', 'Comunicacao com Clientes', 'Command', 'QUICK WIN', '2-3 dias'],
            ['5', 'Agravo de Instrumento', 'Pipeline', 'MEDIO', '1 semana'],
            ['6', 'Preparacao Audiencias', 'Pipeline', 'MEDIO', '4-5 dias'],
            ['7', 'Triagem Novos Casos', 'Pipeline', 'MEDIO', '1 semana'],
            ['8', 'Monitoramento Legislativo', 'Cmd + Cron', 'MEDIO', '1 semana'],
            ['9', 'Pareceres Internos', 'Pipeline', 'MEDIO', '3-4 dias'],
            ['10', 'Verificador Jurisprudencia', 'Skill Global', 'CRITICO', '3-5 dias'],
        ],
        col_widths=[0.8*cm, 4.5*cm, 2.8*cm, 2.5*cm, 2.5*cm]
    ))

    story.append(PageBreak())

    # ──── WORKFLOWS SUGERIDOS COM VALIDADORES ────
    suggested = [
        {
            'num': '1', 'title': 'Gestao de Prazos Processuais',
            'meta': 'Command + Cron Diario  |  CRITICO',
            'trigger': '/prazos hoje | /prazos semana | /prazos criticos | Cron diario 8h',
            'problema': 'Perda de prazo = responsabilidade civil + sancao OAB. Gestao manual e fragil e falha sob pressao.',
            'roi': 'Risco ZERO de perder prazo. Eliminacao de planilhas manuais. Priorizacao automatica da carga.',
            'como_usar': [
                ('Tipo', 'Command (.claude/commands/prazos.md) + Cron Job diario'),
                ('Uso manual', '/prazos hoje, /prazos semana ou /prazos criticos'),
                ('Uso automatico', 'Cron diario 8h executa varredura e envia painel'),
                ('Implementacao', 'Command /prazos + script scripts/prazos_monitor.py'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/prazos (manual) ou cron diario 8h (automatico)', 'type': 'trigger', 'output': ''},
                {'label': 'Varredura [Script]', 'text': 'Script Python varre todos os caso.json e extrai array prazos[]', 'type': 'script', 'output': 'Lista prazos'},
                {'label': 'Calculo [Script]', 'text': 'Calcular dias uteis descontando feriados forenses e recessos (tabela local)', 'type': 'script', 'output': 'Dias restantes'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verificar consistencia: prazo nao pode ser anterior a intimacao, datas fazem sentido?', 'type': 'validate', 'output': 'Dados validados'},
                {'label': 'Classificacao', 'text': 'CRITICO (<3d) | ATENCAO (3-7d) | OK (>7d) + sugestao de pipeline por prazo', 'type': 'script', 'output': 'Semaforo'},
                {'label': 'Output', 'text': 'Painel formatado com semaforo + acao sugerida para cada caso', 'type': 'output', 'output': 'Painel prazos'},
            ],
        },
        {
            'num': '2', 'title': 'Pesquisa Jurisprudencial Sob Demanda',
            'meta': 'Command (agente reutilizado)  |  QUICK WIN',
            'trigger': '/pesquisa "tema" [--tribunal STJ] [--caso NOME]',
            'problema': 'Pesquisa manual em sites de tribunais consome 30-60 min por consulta. Resultado incompleto.',
            'roi': 'Economia 30-60 min/consulta. Agente ja existe — menor esforco de implementacao.',
            'como_usar': [
                ('Tipo', 'Command (.claude/commands/pesquisa.md) — reutiliza agente existente'),
                ('Uso', '/pesquisa "tema". Flags: --tribunal STJ, --caso NOME'),
                ('Implementacao', 'Command /pesquisa invoca pesquisador-jurisprudencial como servico autonomo'),
                ('Output', 'pesquisas/pesquisa_YYYYMMDD.txt. Com --caso, salva na pasta do caso'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/pesquisa "clausula de nao concorrencia em contratos de franquia"', 'type': 'trigger', 'output': 'Query'},
                {'label': 'Pesquisa [Sonnet]', 'text': 'Pesquisador Jurisprudencial (REUTILIZADO) faz web search em sites de tribunais', 'type': 'sonnet', 'output': 'Resultados brutos'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verificar CADA citacao: numero existe? Relator correto? Data confere? Ementa bate?', 'type': 'validate', 'output': 'Citacoes validadas'},
                {'label': 'Filtragem', 'text': 'Remover citacoes nao verificaveis. Marcar incertas com [VERIFICAR]', 'type': 'script', 'output': 'Lista limpa'},
                {'label': 'ANEXAR PETICAO [Sonnet]', 'text': 'OBRIGATORIO: para cada jurisprudencia encontrada, localizar e anexar a peticao que originou o julgado', 'type': 'validate', 'output': 'Peticao anexada'},
                {'label': 'Output', 'text': '5-10 precedentes verificados com tendencia + peticao originaria anexada a cada um', 'type': 'output', 'output': 'pesquisa_*.txt'},
            ],
        },
        {
            'num': '3', 'title': 'Pipeline de Embargos de Declaracao',
            'meta': 'Pipeline Multi-Agente (6 etapas)  |  QUICK WIN',
            'trigger': '/caso embargos [--decisao arquivo.pdf] [--prequestionamento]',
            'problema': 'Peca intermediaria mais frequente. 2-4h manual. Essencial para prequestionamento pre-recurso.',
            'roi': 'R$400-800 economizados por peca. Custo API ~R$6. ROI >60x.',
            'como_usar': [
                ('Tipo', 'Pipeline Multi-Agente via sub-comando /caso embargos'),
                ('Uso', '/caso embargos. Flags: --decisao, --prequestionamento'),
                ('Implementacao', 'Sub-comando no hub /caso + 2 agentes novos + reutiliza revisor-estilo e gerador-docx'),
                ('GATE', 'Advogado revisa texto final antes de gerar .docx'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/caso embargos — identifica ultima decisao no caso.json automaticamente', 'type': 'trigger', 'output': 'caso.json'},
                {'label': 'Analista Vicios [Opus]', 'text': 'Identifica omissoes, obscuridades e contradicoes na decisao judicial', 'type': 'opus', 'output': 'vicios_decisao.txt'},
                {'label': 'Redator Embargos [Opus]', 'text': 'Redige embargos estruturados por vicio, com prequestionamento quando aplicavel', 'type': 'opus', 'output': 'embargos_v1.txt'},
                {'label': 'VALIDADOR Estilo [Sonnet]', 'text': 'Verifica aderencia ao perfil-estilo.md: conectivos, vocabulario, ausencia de anti-patterns', 'type': 'validate', 'output': 'review_estilo.txt'},
                {'label': 'VALIDADOR Juridico [Sonnet]', 'text': 'Verifica: todos os vicios cobertos? Artigos corretos? Citacoes existem? Prequestionamento completo?', 'type': 'validate', 'output': 'review_jur.txt'},
                {'label': 'Auditor Final [Opus]', 'text': 'Consolida v1 + reviews. Aplica correcoes sem novos erros. Texto definitivo', 'type': 'opus', 'output': 'embargos_final.txt'},
                {'label': 'GATE HUMANO', 'text': 'Advogado revisa texto final antes de gerar .docx. Pode editar ou aprovar', 'type': 'gate', 'output': 'GO / EDITAR'},
                {'label': 'Gerador .docx', 'text': 'gerar_peticao.py com identidade visual do escritorio', 'type': 'script', 'output': 'EMBARGOS_*.docx'},
            ],
        },
        {
            'num': '4', 'title': 'Comunicacao com Clientes',
            'meta': 'Command  |  QUICK WIN',
            'trigger': '/caso relatorio CLIENTE | /caso explicar "texto da decisao"',
            'problema': 'Traduzir juridiques para linguagem simples consome tempo. Falta de comunicacao perde clientes.',
            'roi': 'Economia 30-60 min/comunicacao. Cliente informado = cliente retido.',
            'como_usar': [
                ('Tipo', 'Sub-comandos do /caso (agente unico Sonnet)'),
                ('Uso', '/caso relatorio SILVA ou /caso explicar "texto"'),
                ('Implementacao', 'Sub-comandos relatorio e explicar no hub /caso + agente comunicador-cliente.md'),
                ('GATE', 'Advogado SEMPRE revisa antes de enviar ao cliente'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/caso relatorio SILVA ou /caso explicar "texto da decisao"', 'type': 'trigger', 'output': 'Dados caso'},
                {'label': 'Analise [Sonnet]', 'text': 'Le caso.json + ultimos artefatos do pipeline. Contextualiza o andamento', 'type': 'sonnet', 'output': 'Contexto'},
                {'label': 'Geracao [Sonnet]', 'text': 'Gera dois textos: resumo tecnico (arquivo) + resumo cliente (linguagem simples)', 'type': 'sonnet', 'output': '2 textos'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verifica: dados sigilosos expostos? Informacao incorreta? Tom adequado para leigo?', 'type': 'validate', 'output': 'Texto validado'},
                {'label': 'GATE HUMANO', 'text': 'Advogado revisa antes de enviar ao cliente. Pode ajustar tom ou conteudo', 'type': 'gate', 'output': 'Aprovado'},
                {'label': 'Output', 'text': 'Texto pronto para enviar por e-mail/WhatsApp ao cliente', 'type': 'output', 'output': 'relatorio_*.txt'},
            ],
        },
        {
            'num': '5', 'title': 'Pipeline de Agravo de Instrumento',
            'meta': 'Pipeline Multi-Agente (7 etapas)  |  MEDIO',
            'trigger': '/caso agravo [--decisao arquivo.pdf]',
            'problema': 'Decisoes interlocutorias prejudiciais exigem resposta rapida com fundamentacao solida.',
            'roi': 'R$600-1200 economizados por peca. Custo API ~R$10. Prazo curto = velocidade critica.',
            'como_usar': [
                ('Tipo', 'Pipeline Multi-Agente via sub-comando /caso agravo'),
                ('Uso', '/caso agravo. Flag: --decisao arquivo.pdf'),
                ('Implementacao', 'Sub-comando no hub /caso + 2 agentes novos + reutiliza pesquisador e revisor'),
                ('GATE', 'Obrigatorio — advogado valida pedido de efeito suspensivo/ativo'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/caso agravo — identifica decisao interlocutoria no caso.json', 'type': 'trigger', 'output': 'caso.json'},
                {'label': 'Analista Decisao [Opus]', 'text': 'Identifica error in judicando/procedendo, prejuizo concreto, urgencia', 'type': 'opus', 'output': 'analise_dec.txt', 'parallel': True},
                {'label': 'Pesq. Jurisp. [Sonnet]', 'text': 'Jurisprudencia para fumus boni iuris e periculum in mora', 'type': 'sonnet', 'output': 'jurisp.txt', 'parallel': True},
                {'label': 'VALIDADOR Citacoes [Sonnet]', 'text': 'Verificar CADA citacao: numero, relator, data, holding. Remover nao-verificaveis', 'type': 'validate', 'output': 'jurisp_validada.txt'},
                {'label': 'Redator Agravo [Opus]', 'text': 'Redige agravo com pedido de efeito suspensivo/ativo quando cabivel', 'type': 'opus', 'output': 'agravo_v1.txt'},
                {'label': 'VALIDADOR Estilo+Jur [Sonnet]', 'text': 'Revisao dupla: aderencia ao estilo + completude juridica + prequestionamento', 'type': 'validate', 'output': 'reviews.txt'},
                {'label': 'Auditor Final [Opus]', 'text': 'Consolida correcoes. Texto definitivo do agravo', 'type': 'opus', 'output': 'agravo_final.txt'},
                {'label': 'GATE HUMANO', 'text': 'Advogado revisa antes de gerar .docx. Ponto critico: pedido de tutela correto?', 'type': 'gate', 'output': 'GO / EDITAR'},
                {'label': 'Gerador .docx', 'text': 'Documento final pronto para protocolo com identidade visual', 'type': 'script', 'output': 'AGRAVO_*.docx'},
            ],
        },
        {
            'num': '6', 'title': 'Preparacao para Audiencias',
            'meta': 'Pipeline Leve (5 etapas)  |  MEDIO',
            'trigger': '/caso audiencia instrucao|conciliacao|julgamento',
            'problema': '3-6h de preparacao manual na vespera, sob pressao. Risco de esquecer pontos relevantes.',
            'roi': 'Preparacao em 30 min ao inves de 4h. Zero pontos esquecidos.',
            'como_usar': [
                ('Tipo', 'Pipeline Leve via sub-comando /caso audiencia TIPO'),
                ('Uso', '/caso audiencia instrucao ou conciliacao ou julgamento'),
                ('Implementacao', 'Sub-comando no hub /caso + 1 agente novo (estrategista-audiencia) + reutiliza analista-juridico'),
                ('Output', 'Briefing .docx imprimivel em Clientes/<CLIENTE>/audiencias/'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/caso audiencia instrucao — le caso.json + todos os artefatos do pipeline', 'type': 'trigger', 'output': 'caso.json'},
                {'label': 'Analista [Opus]', 'text': 'Resumo do caso, pontos-chave, cronologia, contradicoes da parte adversa', 'type': 'opus', 'output': 'resumo.txt', 'parallel': True},
                {'label': 'Estrategista [Sonnet]', 'text': 'Roteiro de perguntas, argumentos orais, pontos de atencao por tipo de audiencia', 'type': 'sonnet', 'output': 'estrategia.txt', 'parallel': True},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Cruzar briefing com caso.json: todos os fatos cobertos? Provas mencionadas? Testemunhas listadas?', 'type': 'validate', 'output': 'Validado'},
                {'label': 'Consolidador [Sonnet]', 'text': 'Monta briefing de 2-3 paginas: resumo + perguntas + argumentos + riscos', 'type': 'sonnet', 'output': 'briefing.txt'},
                {'label': 'Output .docx', 'text': 'Briefing compacto e imprimivel para levar na audiencia', 'type': 'output', 'output': 'BRIEFING_*.docx'},
            ],
        },
        {
            'num': '7', 'title': 'Triagem de Novos Casos',
            'meta': 'Pipeline (5 etapas)  |  MEDIO',
            'trigger': '/triagem NOME_CLIENTE',
            'problema': '1-3h para avaliar viabilidade. Muitas vezes resulta em declinar — tempo sem retorno.',
            'roi': 'Triagem em 15 min ao inves de 2h. Decisoes baseadas em dados, nao intuicao.',
            'como_usar': [
                ('Tipo', 'Command proprio (.claude/commands/triagem.md) com pipeline'),
                ('Uso', '/triagem NOME_CLIENTE — jogar documentos na pasta antes'),
                ('Implementacao', 'Command /triagem + 2 agentes novos (analista-viabilidade + parecerista) + reutiliza pesquisador'),
                ('Pos-triagem', 'Se aceitar: /novo-caso. Se recusar: pasta como registro'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/triagem SILVA — cria caso.json com status "triagem"', 'type': 'trigger', 'output': 'caso.json'},
                {'label': 'Analista Viabilidade [Opus]', 'text': 'Analisa documentos, identifica teses viaveis, pontos fracos, riscos processuais', 'type': 'opus', 'output': 'analise_viab.txt'},
                {'label': 'Pesq. Jurisp. [Sonnet]', 'text': 'Busca precedentes para cada tese. Calcula taxa de sucesso aproximada', 'type': 'sonnet', 'output': 'precedentes.txt'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verificar citacoes de precedentes. Score faz sentido? Riscos identificados sao reais?', 'type': 'validate', 'output': 'Dados validados'},
                {'label': 'Parecerista [Opus]', 'text': 'Gera parecer: ACEITAR / RECUSAR / NEGOCIAR com score, justificativa e condicoes', 'type': 'opus', 'output': 'parecer_viab.txt'},
                {'label': 'Output', 'text': 'Parecer de 1 pagina com score, teses, riscos e recomendacao objetiva', 'type': 'output', 'output': 'Parecer'},
            ],
        },
        {
            'num': '8', 'title': 'Monitoramento Legislativo Semanal',
            'meta': 'Command + Cron Semanal  |  MEDIO',
            'trigger': '/legislacao semana | /legislacao impacto CASO | Cron semanal (segunda 8h)',
            'problema': 'Mudancas legislativas impactam casos ativos. Acompanhamento manual e falho e inconsistente.',
            'roi': 'Escritorio sempre atualizado. Zero argumentos com legislacao revogada.',
            'como_usar': [
                ('Tipo', 'Command (.claude/commands/legislacao.md) + Cron semanal'),
                ('Uso manual', '/legislacao semana ou /legislacao impacto CASO'),
                ('Uso automatico', 'Cron semanal (segunda 8h) gera relatorio automaticamente'),
                ('Implementacao', 'Command /legislacao + agente monitor-legislativo.md (Sonnet + web search)'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': 'Cron semanal (segunda 8h) ou /legislacao semana', 'type': 'trigger', 'output': ''},
                {'label': 'Pesquisa [Sonnet]', 'text': 'Web search em DOU, informativos STJ/STF, sites legislativos por area de atuacao', 'type': 'sonnet', 'output': 'mudancas.txt'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verificar: lei/sumula citada existe? Data correta? Texto do dispositivo confere?', 'type': 'validate', 'output': 'Mudancas validadas'},
                {'label': 'Cruzamento [Script]', 'text': 'Cruzar mudancas com tipo_acao dos casos ativos em caso.json', 'type': 'script', 'output': 'impactos.txt'},
                {'label': 'Output', 'text': 'Relatorio: "Mudancas que impactam seus casos" com referencia cruzada', 'type': 'output', 'output': 'legislacao_sem.txt'},
            ],
        },
        {
            'num': '9', 'title': 'Pareceres Internos',
            'meta': 'Pipeline Leve (4 etapas)  |  MEDIO',
            'trigger': '/parecer "tema ou questao juridica"',
            'problema': 'Pareceres consomem 2-3h. Raciocinio estrategico fica sem registro formal.',
            'roi': 'Pareceres em 15 min ao inves de 2-3h. Conhecimento documentado.',
            'como_usar': [
                ('Tipo', 'Command proprio (.claude/commands/parecer.md) com pipeline leve'),
                ('Uso', '/parecer "tema". Flag: --caso NOME para vincular a caso'),
                ('Implementacao', 'Command /parecer + 2 agentes novos (analista-tematico + redator-parecer) + reutiliza revisor-estilo'),
                ('Output', 'pareceres/PARECER_TEMA_DATA.docx ou dentro da pasta do caso'),
            ],
            'steps': [
                {'label': 'Trigger', 'text': '/parecer "prescricao intercorrente em execucao fiscal"', 'type': 'trigger', 'output': 'Tema'},
                {'label': 'Analista Tematico [Opus]', 'text': 'Pesquisa aprofundada com web search + jurisprudencia relevante sobre o tema', 'type': 'opus', 'output': 'pesquisa_tema.txt'},
                {'label': 'Redator Parecer [Opus]', 'text': 'Redacao no estilo do escritorio com fundamentacao juridica estruturada', 'type': 'opus', 'output': 'parecer_v1.txt'},
                {'label': 'VALIDADOR [Sonnet]', 'text': 'Verificar citacoes, coerencia argumentativa, completude, aderencia ao estilo', 'type': 'validate', 'output': 'review.txt'},
                {'label': 'Auditor [Opus]', 'text': 'Aplica correcoes do validador. Texto definitivo do parecer', 'type': 'opus', 'output': 'parecer_final.txt'},
                {'label': 'Output .docx', 'text': 'Parecer formatado pronto para arquivo interno', 'type': 'output', 'output': 'PARECER_*.docx'},
            ],
        },
        {
            'num': '10', 'title': 'Verificador de Jurisprudencia (Pre-Protocolo)',
            'meta': 'Skill Global — integravel a TODOS os pipelines  |  CRITICO',
            'trigger': 'Automatico antes de gerar .docx em qualquer pipeline (OBRIGATORIO)',
            'problema': 'Citacao fabricada por IA = sancao OAB + responsabilidade civil. Risco numero 1 do sistema.',
            'roi': 'PREVINE SANCAO OAB. Elimina risco #1. Deve ser implementado ANTES de qualquer outra melhoria.',
            'como_usar': [
                ('Tipo', 'Skill global (.claude/skills/verificador-jurisprudencia/SKILL.md)'),
                ('Uso automatico', 'Roda AUTOMATICAMENTE antes do Gerador .docx em TODOS os pipelines'),
                ('Uso manual', '/verificar-jurisp ARQUIVO.txt para checar qualquer texto'),
                ('Implementacao', 'Skill + script extrair_citacoes.py + modificar TODOS os pipelines existentes'),
                ('GATE', 'Se citacao falhar: BLOQUEIA .docx ate advogado resolver'),
            ],
            'steps': [
                {'label': 'Trigger (AUTOMATICO)', 'text': 'Executado antes da etapa Gerador .docx em TODOS os pipelines do sistema', 'type': 'gate', 'output': 'Texto da peca'},
                {'label': 'Extracao [Script]', 'text': 'Regex + LLM identifica todos os numeros de processo, sumulas e teses citados no texto', 'type': 'script', 'output': 'Lista citacoes'},
                {'label': 'VALIDADOR 1 — Existencia [Sonnet]', 'text': 'Web search CADA numero no STJ/STF/TJ. O processo existe? A decisao existe?', 'type': 'validate', 'output': 'Existe: S/N'},
                {'label': 'VALIDADOR 2 — Holding [Sonnet]', 'text': 'A ementa REAL diz o que a peca afirma? Relator e data batem? Tese correta?', 'type': 'validate', 'output': 'Holding: OK/NOK'},
                {'label': 'VALIDADOR 3 — Vigencia [Sonnet]', 'text': 'A jurisprudencia ainda esta vigente? Foi superada? Houve mudanca de entendimento?', 'type': 'validate', 'output': 'Vigente: S/N'},
                {'label': 'GATE HUMANO OBRIGATORIO', 'text': 'Se QUALQUER citacao nao verificada: marca [VERIFICAR] e BLOQUEIA geracao .docx', 'type': 'gate', 'output': 'GO / BLOQUEIO'},
                {'label': 'Relatorio', 'text': 'Lista completa: citacao | status (OK/VERIFICAR/REMOVIDA) | fonte de verificacao', 'type': 'output', 'output': 'verif_jurisp.txt'},
            ],
        },
    ]

    for wf in suggested:
        story.append(section_header(wf['num'], wf['title']))
        story.append(Spacer(1, 0.2*cm))

        story.append(info_card([
            ('Tipo | Prioridade', wf['meta']),
            ('Trigger', f'<font name="Courier" size="8">{wf["trigger"]}</font>'),
            ('Problema', wf['problema']),
        ]))
        story.append(Spacer(1, 0.3*cm))

        story.append(FlowChart(wf['steps']))
        story.append(Spacer(1, 0.2*cm))

        # ROI box
        roi_data = [[Paragraph(f'<b>ROI:</b> {wf["roi"]}',
                               ParagraphStyle('roi', fontName='Helvetica', fontSize=9, leading=13, textColor=HexColor("#1B7A3D")))]]
        rt = Table(roi_data, colWidths=[16.3*cm])
        rt.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), HexColor("#E8F5EC")),
            ('LEFTPADDING', (0,0),(-1,-1), 10),
            ('TOPPADDING', (0,0),(-1,-1), 6),
            ('BOTTOMPADDING', (0,0),(-1,-1), 6),
            ('LINEBELOW', (0,0),(-1,-1), 1.2, HexColor("#1B7A3D")),
            ('ROUNDEDCORNERS', [3,3,3,3]),
        ]))
        story.append(rt)
        story.append(Spacer(1, 0.3*cm))

        # Como Usar card
        if 'como_usar' in wf:
            story.append(Paragraph('<b>Como Usar</b>', ps('h3', spaceBefore=4)))
            story.append(info_card(wf['como_usar'], bg=HexColor("#EEF2F7")))

        story.append(PageBreak())

    # ═══ PAGINA FINAL ═══
    story.append(Spacer(1, 2*cm))
    story.append(gold_hr())
    story.append(Spacer(1, 0.5*cm))

    story.append(highlight_box(
        '<b>Resumo Final</b><br/><br/>'
        '10 workflows atuais documentados com diagramas visuais.<br/>'
        '10 workflows sugeridos, TODOS com etapas de <font color="#B8860B"><b>VALIDACAO</b></font> obrigatorias.<br/>'
        'Workflows criticos incluem <font color="#C0392B"><b>GATE HUMANO</b></font> pre-protocolo.<br/><br/>'
        '<b>Prioridade absoluta:</b> Workflow #10 (Verificador de Jurisprudencia) deve ser implementado '
        'ANTES de qualquer outro — elimina o risco #1 do sistema (sancao OAB por citacao fabricada).<br/><br/>'
        'O sistema v2.0 cobre ~15-20% das atividades. Com os 10 workflows sugeridos: <b>70-80%</b>.'
    ))

    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(
        '<font size="8" color="#B0B0B0">Documento 07  |  Abril 2026  |  Analise Critica — Sistema de Workflow Juridico  |  '
        'Gastao da Rosa &amp; Moukarzel  |  Confidencial</font>',
        ps('small')
    ))

    doc.build(story)
    sz = os.path.getsize(OUTPUT_PATH)
    print(f"PDF gerado: {OUTPUT_PATH}")
    print(f"Tamanho: {sz / 1024:.0f} KB")
    print(f"Paginas estimadas: ~{len(suggested) + 12}")


if __name__ == "__main__":
    build()
