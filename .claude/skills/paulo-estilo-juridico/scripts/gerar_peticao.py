#!/usr/bin/env python3
"""
Script para gerar peticoes juridicas formatadas em .docx
no padrao do Dr. Paulo Moukarzel Junior.

O arquivo .docx e SEMPRE salvo em: <base-dir>/<nome_cliente>/output_claude/<arquivo>.docx
A pasta do cliente e a subpasta output_claude sao criadas automaticamente se nao existirem.

Uso:
  python gerar_peticao.py --titulo "CONTESTACAO" --cliente "Joao da Silva" \
    --conteudo /tmp/texto.txt

  # Com advogado, OAB e diretorio base:
  python gerar_peticao.py --titulo "HABEAS CORPUS" --cliente "Joao da Silva" \
    --advogado "Paulo Ekke Moukarzel Junior" --oab "12345" \
    --cidade "Florianopolis" --base-dir /caminho/clientes --conteudo /tmp/texto.txt

  # Ou passando o conteudo diretamente (stdin):
  echo "Texto da peticao" | python gerar_peticao.py --titulo "HABEAS CORPUS" \
    --cliente "Joao da Silva"
"""

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print(
        "Erro: a biblioteca 'python-docx' nao esta instalada.\n"
        "Instale com: pip install python-docx\n"
        "Ou use: pip install -r requirements.txt",
        file=__import__('sys').stderr
    )
    __import__('sys').exit(1)

import argparse
import os
import sys
import re
import unicodedata
from datetime import datetime


def configurar_documento():
    """Configura documento Word com padrao forense."""
    doc = Document()

    # Margens (padrao forense: 3cm esquerda, 2cm direita, 3cm superior, 2cm inferior)
    sections = doc.sections
    for section in sections:
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.page_width = Cm(21)   # A4
        section.page_height = Cm(29.7)

    # Estilo Normal
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(12)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.line_spacing = Pt(18)  # 1.5
    normal.paragraph_format.space_after = Pt(6)

    # Adicionar numeracao de paginas no footer
    adicionar_numeracao_paginas(doc)

    return doc


def adicionar_numeracao_paginas(doc):
    """Adiciona 'Pagina X de Y' centralizado no rodape, Arial 9pt."""
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # "Pagina "
        run_pre = paragraph.add_run("Pagina ")
        run_pre.font.name = 'Arial'
        run_pre.font.size = Pt(9)

        # Campo PAGE (numero da pagina atual)
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        run_page = paragraph.add_run()
        run_page._r.append(fldChar1)

        instrText1 = OxmlElement('w:instrText')
        instrText1.set(qn('xml:space'), 'preserve')
        instrText1.text = ' PAGE '
        run_page2 = paragraph.add_run()
        run_page2._r.append(instrText1)

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        run_page3 = paragraph.add_run()
        run_page3._r.append(fldChar2)

        # " de "
        run_mid = paragraph.add_run(" de ")
        run_mid.font.name = 'Arial'
        run_mid.font.size = Pt(9)

        # Campo NUMPAGES (total de paginas)
        fldChar3 = OxmlElement('w:fldChar')
        fldChar3.set(qn('w:fldCharType'), 'begin')
        run_total = paragraph.add_run()
        run_total._r.append(fldChar3)

        instrText2 = OxmlElement('w:instrText')
        instrText2.set(qn('xml:space'), 'preserve')
        instrText2.text = ' NUMPAGES '
        run_total2 = paragraph.add_run()
        run_total2._r.append(instrText2)

        fldChar4 = OxmlElement('w:fldChar')
        fldChar4.set(qn('w:fldCharType'), 'end')
        run_total3 = paragraph.add_run()
        run_total3._r.append(fldChar4)


def adicionar_paragrafo(doc, texto, bold=False, italico=False, tamanho=12,
                         alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, espaco_antes=0,
                         espaco_depois=6, centralizado=False):
    """Adiciona paragrafo formatado."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if centralizado else alinhamento
    p.paragraph_format.space_before = Pt(espaco_antes)
    p.paragraph_format.space_after = Pt(espaco_depois)
    p.paragraph_format.line_spacing = Pt(18)
    adicionar_texto_com_formatacao(p, texto, bold_base=bold, italic_base=italico, tamanho=tamanho)
    return p


def adicionar_texto_com_formatacao(paragraph, texto, bold_base=False, italic_base=False, tamanho=12):
    """
    Parseia markdown **negrito** e *italico* no texto e adiciona runs formatados.

    Suporta:
    - **texto** -> negrito
    - *texto* -> italico
    - ***texto*** -> negrito + italico
    - texto normal
    """
    # Regex para capturar ***bold+italic***, **bold**, *italic*, e texto normal
    pattern = re.compile(r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*)')

    last_end = 0
    for match in pattern.finditer(texto):
        # Adicionar texto antes do match como run normal
        if match.start() > last_end:
            run = paragraph.add_run(texto[last_end:match.start()])
            run.font.name = 'Arial'
            run.font.size = Pt(tamanho)
            run.bold = bold_base
            run.italic = italic_base

        # Determinar tipo de formatacao
        if match.group(2):  # ***bold+italic***
            run = paragraph.add_run(match.group(2))
            run.bold = True
            run.italic = True
        elif match.group(3):  # **bold**
            run = paragraph.add_run(match.group(3))
            run.bold = True
            run.italic = italic_base
        elif match.group(4):  # *italic*
            run = paragraph.add_run(match.group(4))
            run.bold = bold_base
            run.italic = True

        run.font.name = 'Arial'
        run.font.size = Pt(tamanho)
        last_end = match.end()

    # Adicionar texto restante apos o ultimo match
    if last_end < len(texto):
        run = paragraph.add_run(texto[last_end:])
        run.font.name = 'Arial'
        run.font.size = Pt(tamanho)
        run.bold = bold_base
        run.italic = italic_base


def processar_texto(doc, texto):
    """
    Processa o texto da peticao e aplica formatacao inteligente.
    - Linhas em MAIUSCULAS sao tratadas como cabecalhos de secao
    - Linhas entre aspas sao recuadas (citacoes)
    - Markdown **negrito** e *italico* sao processados
    - Demais linhas sao paragrafos normais
    """
    linhas = texto.split('\n')
    em_citacao = False
    buffer_citacao = []

    def flush_citacao():
        if buffer_citacao:
            citacao = ' '.join(buffer_citacao).strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(2.5)
            p.paragraph_format.right_indent = Cm(2.5)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = Pt(15)
            adicionar_texto_com_formatacao(p, citacao, italic_base=True, tamanho=11)
            buffer_citacao.clear()

    for linha in linhas:
        stripped = linha.strip()
        if not stripped:
            flush_citacao()
            em_citacao = False
            continue

        # Detectar inicio/fim de bloco de citacao (linha com aspas ou recuo)
        if stripped.startswith('"') or stripped.startswith('\u201c'):
            em_citacao = True

        if em_citacao:
            buffer_citacao.append(stripped.strip('"').strip('\u201c').strip('\u201d'))
            if stripped.endswith('"') or stripped.endswith('\u201d') or stripped.endswith(')'):
                flush_citacao()
                em_citacao = False
            continue

        flush_citacao()

        # Cabecalho de secao (ex: "I – DOS FATOS" ou "II – DO DIREITO")
        if re.match(r'^[IVX]+\s*[\u2013\u2014-]\s*[A-Z]', stripped) or re.match(r'^\d+\.\d*\s+[A-Z]', stripped):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            adicionar_texto_com_formatacao(p, stripped, bold_base=True, tamanho=12)
            continue

        # Linha com APENAS MAIUSCULAS (titulo/enderecamento)
        if stripped.isupper() and len(stripped) > 3:
            p = doc.add_paragraph()
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            adicionar_texto_com_formatacao(p, stripped, bold_base=True, tamanho=12)
            continue

        # Paragrafo de pedidos (comeca com letra + ")")
        if re.match(r'^[a-z]\)', stripped) or re.match(r'^\d+\)', stripped):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.5)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = Pt(18)
            adicionar_texto_com_formatacao(p, stripped, tamanho=12)
            continue

        # Paragrafo normal (com suporte a markdown bold/italic)
        adicionar_paragrafo(doc, stripped, espaco_antes=0, espaco_depois=6)


def _sanitizar_nome(nome):
    """Remove acentos e caracteres especiais para usar como nome de pasta/arquivo."""
    # Remover acentos
    nfkd = unicodedata.normalize('NFKD', nome)
    sem_acento = ''.join(c for c in nfkd if not unicodedata.combining(c))
    # Substituir espacos por underscore, remover caracteres invalidos
    sanitizado = re.sub(r'[^\w\s-]', '', sem_acento).strip()
    sanitizado = re.sub(r'[\s]+', '_', sanitizado)
    return sanitizado.upper()


def _construir_output_path(cliente, titulo, base_dir=None):
    """
    Constroi o caminho de output obrigatorio:
    <base_dir>/<nome_cliente>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx

    Cria as pastas automaticamente se nao existirem.
    """
    if base_dir is None:
        base_dir = os.getcwd()

    nome_pasta_cliente = _sanitizar_nome(cliente)
    nome_titulo = _sanitizar_nome(titulo)
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    nome_arquivo = f"{nome_titulo}_{nome_pasta_cliente}_{data_hoje}.docx"

    pasta_output = os.path.join(base_dir, nome_pasta_cliente, 'output_claude')
    os.makedirs(pasta_output, exist_ok=True)

    return os.path.join(pasta_output, nome_arquivo)


def _data_por_extenso():
    """Retorna a data atual por extenso no formato juridico brasileiro."""
    meses = {
        1: 'janeiro', 2: 'fevereiro', 3: 'marco', 4: 'abril',
        5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
        9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
    }
    hoje = datetime.now()
    return f"{hoje.day} de {meses[hoje.month]} de {hoje.year}"


def _conteudo_ja_tem_data(conteudo):
    """Verifica se o conteudo ja contem bloco de data/encerramento."""
    ultimas_linhas = conteudo.strip().split('\n')[-5:]
    texto_final = '\n'.join(ultimas_linhas).lower()
    # Detectar padroes comuns de data no encerramento
    if re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', texto_final):
        return True
    if re.search(r'pede\s+deferimento', texto_final):
        return True
    return False


def gerar_peticao(titulo, conteudo, cliente, cidade='Florianopolis',
                  advogado=None, oab=None, base_dir=None):
    """
    Gera o arquivo .docx da peticao.

    O arquivo e SEMPRE salvo em: <base_dir>/<CLIENTE>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx
    """
    # Construir caminho obrigatorio
    output_path = _construir_output_path(cliente, titulo, base_dir)

    doc = configurar_documento()

    # Gravar cliente como metadata do documento
    doc.core_properties.subject = f"Cliente: {cliente}"

    # Titulo da peca (centralizado, negrito, maiusculas)
    p_titulo = doc.add_paragraph()
    p_titulo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_titulo.paragraph_format.space_before = Pt(0)
    p_titulo.paragraph_format.space_after = Pt(18)
    run = p_titulo.add_run(titulo.upper())
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.bold = True

    # Linha separadora
    doc.add_paragraph()

    # Processar o conteudo
    processar_texto(doc, conteudo)

    # Bloco de encerramento: cidade, data e assinatura (se nao ja presente)
    if not _conteudo_ja_tem_data(conteudo):
        doc.add_paragraph()  # espaco antes do encerramento

        # Cidade e data
        p_data = doc.add_paragraph()
        p_data.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_data.paragraph_format.space_before = Pt(12)
        p_data.paragraph_format.space_after = Pt(18)
        run_data = p_data.add_run(f"{cidade}, {_data_por_extenso()}.")
        run_data.font.name = 'Arial'
        run_data.font.size = Pt(12)

    # Assinatura do advogado (se fornecido)
    if advogado:
        p_adv = doc.add_paragraph()
        p_adv.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_adv.paragraph_format.space_before = Pt(24)
        p_adv.paragraph_format.space_after = Pt(2)
        run_adv = p_adv.add_run(advogado)
        run_adv.font.name = 'Arial'
        run_adv.font.size = Pt(12)
        run_adv.bold = True

        if oab:
            p_oab = doc.add_paragraph()
            p_oab.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_oab.paragraph_format.space_before = Pt(0)
            p_oab.paragraph_format.space_after = Pt(6)
            run_oab = p_oab.add_run(f"OAB/SC n. {oab}")
            run_oab.font.name = 'Arial'
            run_oab.font.size = Pt(12)

    # Salvar
    doc.save(output_path)
    print(f"Peticao gerada: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Gera peticao juridica formatada em .docx. '
                    'O arquivo e salvo em <base-dir>/<CLIENTE>/output_claude/<TIPO>_<CLIENTE>_<DATA>.docx'
    )
    parser.add_argument('--titulo', required=True, help='Tipo da peca (ex: CONTESTACAO)')
    parser.add_argument('--cliente', required=True,
                        help='Nome do cliente (OBRIGATORIO — usado para criar a pasta e metadata)')
    parser.add_argument('--conteudo', help='Caminho para arquivo de texto com o conteudo')
    parser.add_argument('--base-dir', default=None,
                        help='Diretorio base onde criar a pasta do cliente (default: diretorio atual)')
    parser.add_argument('--cidade', default='Florianopolis',
                        help='Cidade para o encerramento (default: Florianopolis)')
    parser.add_argument('--advogado', required=False, default=None,
                        help='Nome do advogado para a linha de assinatura')
    parser.add_argument('--oab', required=False, default=None,
                        help='Numero da OAB para a linha de assinatura')
    args = parser.parse_args()

    # Ler conteudo
    if args.conteudo:
        with open(args.conteudo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    else:
        # Ler do stdin
        conteudo = sys.stdin.read()

    if not conteudo.strip():
        print("Erro: nenhum conteudo fornecido.", file=sys.stderr)
        sys.exit(1)

    gerar_peticao(
        titulo=args.titulo,
        conteudo=conteudo,
        cliente=args.cliente,
        cidade=args.cidade,
        advogado=args.advogado,
        oab=args.oab,
        base_dir=args.base_dir
    )


if __name__ == '__main__':
    main()
