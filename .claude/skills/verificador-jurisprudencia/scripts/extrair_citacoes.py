#!/usr/bin/env python3
"""Extrai citacoes de jurisprudencia de textos juridicos."""
import re, json, sys, argparse
from pathlib import Path

# Padroes CNJ e tribunais
PATTERNS = [
    # REsp, RE, HC, RHC, AREsp, AgRg, AgInt, EDcl
    (r"((?:REsp|RE|HC|RHC|AREsp|AgRg|AgInt|EDcl)\s*(?:n[.ºo]*\s*)?[\d.,/\-]+)", "recurso"),
    # Sumula N ou Sumula Vinculante N
    (r"(S[uú]mula\s+(?:Vinculante\s+)?n?[.ºo]*\s*\d+)", "sumula"),
    # Tema N (repercussao geral)
    (r"(Tema\s+(?:n[.ºo]*\s*)?[\d.]+)", "tema"),
    # Citacao inline com Min./Rel.
    (r"\(([^)]*(?:Min\.|Rel\.)[^)]*(?:julg|DJ|DJe)[^)]*)\)", "citacao_inline"),
]


def extrair(texto: str) -> list[dict]:
    citacoes = []
    seen = set()
    for linha_num, linha in enumerate(texto.splitlines(), 1):
        for pattern, tipo in PATTERNS:
            for match in re.finditer(pattern, linha, re.IGNORECASE):
                raw = match.group(1).strip()
                key = re.sub(r"\s+", " ", raw.lower())
                if key not in seen:
                    seen.add(key)
                    citacoes.append({
                        "tipo": tipo,
                        "texto": raw,
                        "linha": linha_num,
                        "contexto": linha.strip()[:200],
                        "status": "pendente"
                    })
    return citacoes


def main():
    parser = argparse.ArgumentParser(description="Extrai citacoes de jurisprudencia")
    parser.add_argument("arquivo", help="Caminho do arquivo .txt para analisar")
    parser.add_argument("--output", help="Caminho do JSON de saida (default: stdout)")
    args = parser.parse_args()

    texto = Path(args.arquivo).read_text(encoding="utf-8")
    resultado = extrair(texto)

    output = json.dumps({"total": len(resultado), "citacoes": resultado},
                        ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Extraidas {len(resultado)} citacoes -> {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
