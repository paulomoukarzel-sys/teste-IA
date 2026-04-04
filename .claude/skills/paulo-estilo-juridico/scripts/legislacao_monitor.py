#!/usr/bin/env python3
"""Monitor legislativo — cruza mudancas legislativas com casos ativos."""
import json, sys, argparse
from pathlib import Path
from datetime import date

# Mapeamento tipo_acao → areas legislativas relevantes
AREAS_POR_TIPO = {
    "contestacao": ["processual civil", "direito civil", "consumidor"],
    "resp": ["processual civil", "direito civil", "recursal"],
    "re": ["constitucional", "processual civil"],
    "aresp": ["processual civil", "recursal"],
    "apelacao": ["processual civil", "direito civil"],
    "embargos": ["processual civil"],
    "agravo": ["processual civil"],
    "hc": ["penal", "processual penal", "constitucional"],
    "inicial": ["direito civil", "consumidor", "trabalhista"],
}

# Palavras-chave por area para matching
KEYWORDS_POR_AREA = {
    "processual civil": ["CPC", "codigo de processo civil", "procedimento", "recurso", "prazo", "tutela"],
    "direito civil": ["codigo civil", "responsabilidade civil", "dano moral", "contrato", "obrigacao"],
    "consumidor": ["CDC", "codigo de defesa do consumidor", "fornecedor", "produto", "servico"],
    "constitucional": ["constituicao", "CF", "direito fundamental", "garantia", "supremo"],
    "recursal": ["recurso especial", "recurso extraordinario", "admissibilidade", "prequestionamento"],
    "penal": ["codigo penal", "CP", "crime", "pena", "dosimetria"],
    "processual penal": ["CPP", "codigo de processo penal", "prisao", "liberdade"],
    "trabalhista": ["CLT", "trabalho", "empregado", "empregador", "rescisao"],
}


def escanear_casos_ativos(base_dir: Path) -> list[dict]:
    """Escaneia caso.json ativos e extrai tipo_acao."""
    casos = []
    clientes_dir = base_dir / "Clientes"
    if not clientes_dir.exists():
        return casos

    for caso_file in sorted(clientes_dir.glob("*/caso.json")):
        try:
            data = json.loads(caso_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        status = data.get("status", "ativo")
        if status in ("concluido", "arquivado", "recusado"):
            continue

        tipo_acao = data.get("tipo_acao") or data.get("prazo_tipo", "")
        casos.append({
            "cliente": data.get("cliente_curto", data.get("cliente", caso_file.parent.name)),
            "tipo_acao": tipo_acao,
            "areas": AREAS_POR_TIPO.get(tipo_acao, ["geral"]),
            "pasta": str(caso_file.parent),
        })

    return casos


def cruzar_com_mudancas(casos: list[dict], mudancas_file: Path) -> list[dict]:
    """Cruza mudancas legislativas com casos ativos."""
    alertas = []

    if not mudancas_file.exists():
        return alertas

    texto_mudancas = mudancas_file.read_text(encoding="utf-8").lower()

    for caso in casos:
        impactos = []
        for area in caso["areas"]:
            keywords = KEYWORDS_POR_AREA.get(area, [])
            matches = [kw for kw in keywords if kw.lower() in texto_mudancas]
            if matches:
                impactos.append({
                    "area": area,
                    "keywords_encontradas": matches,
                })

        if impactos:
            alertas.append({
                "cliente": caso["cliente"],
                "tipo_acao": caso["tipo_acao"],
                "impactos": impactos,
                "pasta": caso["pasta"],
            })

    return alertas


def formatar_relatorio(casos: list[dict], alertas: list[dict], hoje: date) -> str:
    """Formata relatorio de cruzamento legislativo."""
    linhas = []
    linhas.append("=" * 80)
    linhas.append(f"CRUZAMENTO LEGISLATIVO — {hoje.strftime('%d/%m/%Y')}")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append(f"Casos ativos escaneados: {len(casos)}")
    linhas.append(f"Casos com potencial impacto: {len(alertas)}")
    linhas.append("")

    if not alertas:
        linhas.append("Nenhum impacto legislativo detectado nos casos ativos.")
    else:
        linhas.append("ALERTAS DE IMPACTO:")
        linhas.append("-" * 80)
        for alerta in alertas:
            linhas.append(f"\n  Cliente: {alerta['cliente']}")
            linhas.append(f"  Tipo: {alerta['tipo_acao']}")
            for imp in alerta["impactos"]:
                linhas.append(f"  Area: {imp['area']} — Keywords: {', '.join(imp['keywords_encontradas'])}")
            linhas.append(f"  Pasta: {alerta['pasta']}")

    linhas.append("")
    linhas.append("=" * 80)
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor legislativo — cruza mudancas com casos ativos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base", default=".", help="Diretorio base do projeto")
    parser.add_argument("--mudancas", default=None,
                        help="Arquivo de mudancas legislativas (default: data/legislacao_semanal_*.txt mais recente)")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    args = parser.parse_args()

    hoje = date.today()
    base = Path(args.base)

    # Encontrar arquivo de mudancas
    if args.mudancas:
        mudancas_file = Path(args.mudancas)
    else:
        data_dir = base / "data"
        if data_dir.exists():
            files = sorted(data_dir.glob("legislacao_semanal_*.txt"), reverse=True)
            mudancas_file = files[0] if files else Path("__nao_existe__")
        else:
            mudancas_file = Path("__nao_existe__")

    casos = escanear_casos_ativos(base)
    alertas = cruzar_com_mudancas(casos, mudancas_file)

    if args.json:
        print(json.dumps({"casos_escaneados": len(casos), "alertas": alertas},
                         ensure_ascii=False, indent=2))
    else:
        print(formatar_relatorio(casos, alertas, hoje))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
