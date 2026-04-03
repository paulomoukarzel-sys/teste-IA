#!/usr/bin/env python3
"""
indexar_vf.py — Indexa arquivos _vf.docx (modelos de peças finalizadas) nas
pastas de clientes e gera data/indice_vf.json com classificação por tipo de peça.

Uso:
    python indexar_vf.py
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

# Raiz do projeto (dois níveis acima de scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

PASTAS_SCAN = [
    PROJECT_ROOT / "Clientes",
    Path(r"C:\Users\paulo\OneDrive\Documentos\M.Adv"),
]

OUTPUT_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = OUTPUT_DIR / "indice_vf.json"

# Ordem de verificação importa: regras mais específicas primeiro
TIPOS = [
    ("AREsp",     re.compile(r"aresp", re.IGNORECASE)),
    ("RHC",       re.compile(r"\brhc\b", re.IGNORECASE)),
    ("REsp",      re.compile(r"\bresp\b|recurso.?especial", re.IGNORECASE)),
    ("RE",        re.compile(r"\b re \b|recurso.?extraordin", re.IGNORECASE)),
    ("HC",        re.compile(r"\bhc\b|habeas", re.IGNORECASE)),
    ("Contestacao", re.compile(r"contesta[cç][aã]o", re.IGNORECASE)),
    ("Apelacao",  re.compile(r"apela[cç][aã]o", re.IGNORECASE)),
    ("Embargos",  re.compile(r"embargos", re.IGNORECASE)),
]


def classificar(nome_arquivo: str) -> str:
    """Retorna o tipo da peça com base no nome do arquivo."""
    for tipo, pattern in TIPOS:
        if pattern.search(nome_arquivo):
            return tipo
    return "Outros"


def extrair_cliente(path: Path) -> str:
    """
    Extrai o nome do cliente a partir da hierarquia de pastas.

    Estratégia:
    1. Se o caminho passa por uma pasta "Clientes", retorna o nome da pasta
       imediatamente abaixo de "Clientes/" (que é sempre o cliente).
    2. Caso contrário, usa o primeiro pai que não seja uma pasta genérica
       conhecida (pipeline, HC, etc.).
    """
    PASTAS_RAIZ_CLIENTES = {"clientes"}
    PASTAS_GENERICAS = {
        "pipeline", "output_claude", "peças", "pecas", "recursos", "docs",
        "processos", "01 - atuações encerradas", "atuações encerradas",
    }

    parts = path.parts
    # Procura âncora "Clientes" no path
    for i, parte in enumerate(parts):
        if parte.lower() in PASTAS_RAIZ_CLIENTES:
            # O próximo segmento é o nome do cliente (se existir)
            if i + 1 < len(parts) - 1:  # não pode ser o arquivo em si
                return parts[i + 1]
            break

    # Fallback: sobe até achar pasta não genérica
    for i in range(len(parts) - 2, 0, -1):
        candidate = parts[i]
        if candidate.lower() not in PASTAS_GENERICAS:
            return candidate
    return path.parent.name


def escanear_pasta(pasta: Path) -> list[dict]:
    """Varre recursivamente a pasta buscando arquivos _vf.docx."""
    resultados = []
    if not pasta.exists():
        print(f"  [aviso] Pasta não encontrada: {pasta}")
        return resultados

    for item in pasta.rglob("*.docx"):
        if "_vf" not in item.stem.lower():
            continue
        try:
            mtime = item.stat().st_mtime
            modificado_em = datetime.fromtimestamp(mtime).isoformat(timespec="seconds")
        except OSError:
            modificado_em = None

        cliente = extrair_cliente(item)
        tipo = classificar(item.name)

        resultados.append({
            "tipo": tipo,
            "cliente": cliente,
            "arquivo": item.name,
            "path": str(item),
            "modificado_em": modificado_em,
        })

    return resultados


def main():
    print("=" * 60)
    print("Indexador de peças _vf.docx")
    print(f"Raiz do projeto: {PROJECT_ROOT}")
    print("=" * 60)

    todos = []
    for pasta in PASTAS_SCAN:
        print(f"\nEscaneando: {pasta}")
        encontrados = escanear_pasta(pasta)
        print(f"  → {len(encontrados)} arquivo(s) encontrado(s)")
        todos.extend(encontrados)

    # Organizar por tipo
    por_tipo: dict[str, list] = {t: [] for t, _ in TIPOS}
    por_tipo["Outros"] = []

    for item in todos:
        tipo = item.pop("tipo")
        por_tipo[tipo].append(item)

    # Ordenar cada lista: mais recente primeiro
    for tipo in por_tipo:
        por_tipo[tipo].sort(
            key=lambda x: x.get("modificado_em") or "",
            reverse=True,
        )

    # Remover tipos vazios do JSON final
    por_tipo_filtrado = {t: v for t, v in por_tipo.items() if v}

    resultado = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "total": len(todos),
        "por_tipo": por_tipo_filtrado,
    }

    # Criar pasta data/ se necessário
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    # Resumo
    print("\n" + "=" * 60)
    print(f"Total de arquivos _vf indexados: {len(todos)}")
    print("-" * 40)
    for tipo, itens in sorted(por_tipo_filtrado.items()):
        print(f"  {tipo:<15} {len(itens):>4} arquivo(s)")
    print("-" * 40)
    print(f"JSON salvo em: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
