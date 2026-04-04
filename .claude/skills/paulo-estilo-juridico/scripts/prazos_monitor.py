#!/usr/bin/env python3
"""Monitor de prazos processuais — escaneia caso.json e classifica por urgencia."""
import json, sys, argparse
from pathlib import Path
from datetime import date, timedelta

# Feriados federais BR (fixos)
FERIADOS_FIXOS = [
    (1, 1),    # Confraternizacao Universal
    (4, 21),   # Tiradentes
    (5, 1),    # Dia do Trabalho
    (9, 7),    # Independencia
    (10, 12),  # N. Sra. Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamacao da Republica
    (12, 25),  # Natal
]

# Feriados estaduais SC
FERIADOS_SC = [
    (8, 11),   # Dia de Santa Catarina
]

# Recesso forense: 20/dez a 20/jan (inclusive)
RECESSO_INICIO_MES, RECESSO_INICIO_DIA = 12, 20
RECESSO_FIM_MES, RECESSO_FIM_DIA = 1, 20


def _pascoa(ano: int) -> date:
    """Calcula data da Pascoa pelo algoritmo de Meeus/Jones/Butcher."""
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return date(ano, mes, dia + 1)


def feriados_moveis(ano: int) -> list[date]:
    """Retorna Sexta-feira Santa e Corpus Christi para o ano."""
    pascoa = _pascoa(ano)
    sexta_santa = pascoa - timedelta(days=2)
    corpus_christi = pascoa + timedelta(days=60)
    return [sexta_santa, corpus_christi]


def em_recesso(d: date) -> bool:
    """Verifica se a data esta no recesso forense (20/dez a 20/jan)."""
    if d.month == 12 and d.day >= RECESSO_INICIO_DIA:
        return True
    if d.month == 1 and d.day <= RECESSO_FIM_DIA:
        return True
    return False


def eh_feriado(d: date) -> bool:
    """Verifica se a data e feriado (federal, estadual SC ou movel)."""
    md = (d.month, d.day)
    if md in FERIADOS_FIXOS or md in FERIADOS_SC:
        return True
    if d in feriados_moveis(d.year):
        return True
    return False


def eh_dia_util(d: date) -> bool:
    """Verifica se a data e dia util forense."""
    if d.weekday() >= 5:  # sabado/domingo
        return False
    if eh_feriado(d):
        return False
    if em_recesso(d):
        return False
    return True


def dias_uteis_entre(inicio: date, fim: date) -> int:
    """Conta dias uteis entre inicio (exclusive) e fim (inclusive)."""
    if fim <= inicio:
        # Prazo vencido — contar dias uteis negativos
        count = 0
        d = fim + timedelta(days=1)
        while d <= inicio:
            if eh_dia_util(d):
                count -= 1
            d += timedelta(days=1)
        return count

    count = 0
    d = inicio + timedelta(days=1)
    while d <= fim:
        if eh_dia_util(d):
            count += 1
        d += timedelta(days=1)
    return count


def classificar(dias: int) -> str:
    """Classifica urgencia baseado em dias uteis restantes."""
    if dias < 0:
        return "VENCIDO"
    elif dias <= 2:
        return "CRITICO"
    elif dias <= 7:
        return "ATENCAO"
    else:
        return "OK"


def semaforo(classificacao: str) -> str:
    """Retorna indicador visual."""
    return {
        "VENCIDO": "[!!!]",
        "CRITICO": "[!! ]",
        "ATENCAO": "[!  ]",
        "OK":      "[   ]",
    }.get(classificacao, "[???]")


def escanear_casos(base_dir: Path) -> list[dict]:
    """Escaneia todos os caso.json em Clientes/*/caso.json."""
    casos = []
    clientes_dir = base_dir / "Clientes"
    if not clientes_dir.exists():
        return casos

    for caso_file in sorted(clientes_dir.glob("*/caso.json")):
        try:
            data = json.loads(caso_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        # Suportar campo prazos[] (novo) e prazo_fatal (legado)
        prazos_list = data.get("prazos", [])
        prazo_fatal = data.get("prazo_fatal")

        if prazos_list:
            for p in prazos_list:
                if p.get("status") == "cumprido":
                    continue
                try:
                    dt = date.fromisoformat(p["data"])
                except (ValueError, KeyError):
                    continue
                casos.append({
                    "cliente": data.get("cliente_curto", data.get("cliente", caso_file.parent.name)),
                    "processo": data.get("processo", "—"),
                    "tipo": p.get("tipo", data.get("prazo_tipo", "—")),
                    "prazo_fatal": p["data"],
                    "descricao": p.get("descricao", ""),
                    "pasta": str(caso_file.parent),
                })
        elif prazo_fatal:
            try:
                date.fromisoformat(prazo_fatal)
            except ValueError:
                continue
            casos.append({
                "cliente": data.get("cliente_curto", data.get("cliente", caso_file.parent.name)),
                "processo": data.get("processo", "—"),
                "tipo": data.get("prazo_tipo", "—"),
                "prazo_fatal": prazo_fatal,
                "descricao": "",
                "pasta": str(caso_file.parent),
            })

    return casos


def formatar_tabela(casos_classificados: list[dict], hoje: date) -> str:
    """Formata tabela de prazos para exibicao."""
    if not casos_classificados:
        return "Nenhum prazo encontrado.\n"

    linhas = []
    linhas.append("=" * 95)
    linhas.append(f"PRAZOS PROCESSUAIS — {hoje.strftime('%d/%m/%Y')}")
    linhas.append("=" * 95)
    linhas.append("")
    linhas.append(f"{'Sem.':<7} {'Cliente':<22} {'Tipo':<15} {'Prazo':<12} {'Dias':<6} {'Class.':<10} {'Processo'}")
    linhas.append("-" * 95)

    for c in casos_classificados:
        dt = date.fromisoformat(c["prazo_fatal"])
        prazo_fmt = dt.strftime("%d/%m/%Y")
        linhas.append(
            f"{c['semaforo']:<7} {c['cliente'][:21]:<22} {c['tipo'][:14]:<15} "
            f"{prazo_fmt:<12} {c['dias_uteis']:<6} {c['classificacao']:<10} {c['processo'][:25]}"
        )

    linhas.append("-" * 95)

    # Resumo
    total = len(casos_classificados)
    vencidos = sum(1 for c in casos_classificados if c["classificacao"] == "VENCIDO")
    criticos = sum(1 for c in casos_classificados if c["classificacao"] == "CRITICO")
    atencao = sum(1 for c in casos_classificados if c["classificacao"] == "ATENCAO")
    ok = sum(1 for c in casos_classificados if c["classificacao"] == "OK")

    linhas.append(f"Total: {total}  |  Vencidos: {vencidos}  |  Criticos: {criticos}  |  Atencao: {atencao}  |  OK: {ok}")
    linhas.append("=" * 95)

    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor de prazos processuais",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Sub-comandos:\n  hoje      Prazos vencendo hoje\n  semana    Proximos 7 dias uteis\n  criticos  Apenas CRITICO + VENCIDO\n  todos     Todos os prazos ordenados por urgencia"
    )
    parser.add_argument("filtro", nargs="?", default="todos",
                        choices=["hoje", "semana", "criticos", "todos"],
                        help="Filtro de exibicao (default: todos)")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    parser.add_argument("--base", default=".", help="Diretorio base do projeto")
    args = parser.parse_args()

    hoje = date.today()
    base = Path(args.base)
    casos = escanear_casos(base)

    # Classificar cada caso
    classificados = []
    for c in casos:
        dt = date.fromisoformat(c["prazo_fatal"])
        dias = dias_uteis_entre(hoje, dt)
        cls = classificar(dias)
        classificados.append({
            **c,
            "dias_uteis": dias,
            "classificacao": cls,
            "semaforo": semaforo(cls),
        })

    # Filtrar
    if args.filtro == "hoje":
        classificados = [c for c in classificados if c["prazo_fatal"] == str(hoje)]
    elif args.filtro == "semana":
        classificados = [c for c in classificados if 0 <= c["dias_uteis"] <= 7]
    elif args.filtro == "criticos":
        classificados = [c for c in classificados if c["classificacao"] in ("CRITICO", "VENCIDO")]

    # Ordenar: VENCIDO primeiro (mais recente), depois por dias_uteis crescente
    ordem = {"VENCIDO": 0, "CRITICO": 1, "ATENCAO": 2, "OK": 3}
    classificados.sort(key=lambda c: (ordem.get(c["classificacao"], 9), c["dias_uteis"]))

    if args.json:
        print(json.dumps(classificados, ensure_ascii=False, indent=2))
    else:
        print(formatar_tabela(classificados, hoje))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
