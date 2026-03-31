"""Wrapper do gerar_peticao.py para geracao de .docx."""

import asyncio
import sys
from pathlib import Path
from backend.config import CLIENTES_DIR, ADVOGADO_NOME, ADVOGADO_OAB, ADVOGADO_CIDADE

# Adicionar o diretorio dos scripts ao path
_scripts_dir = Path(__file__).resolve().parent.parent.parent / ".claude" / "skills" / "paulo-estilo-juridico" / "scripts"
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from gerar_peticao import gerar_peticao


async def generate_docx(
    titulo: str,
    conteudo: str,
    cliente: str,
    cidade: str | None = None,
    advogado: str | None = None,
    oab: str | None = None,
) -> dict:
    """
    Gera .docx usando gerar_peticao.py via executor (nao bloqueia event loop).

    Returns:
        dict com file_path, file_name, status
    """
    cidade = cidade or ADVOGADO_CIDADE
    advogado = advogado or ADVOGADO_NOME
    oab = oab or ADVOGADO_OAB

    loop = asyncio.get_event_loop()

    try:
        output_path = await loop.run_in_executor(
            None,
            lambda: gerar_peticao(
                titulo=titulo,
                conteudo=conteudo,
                cliente=cliente,
                cidade=cidade,
                advogado=advogado,
                oab=oab,
                base_dir=str(CLIENTES_DIR),
            )
        )

        return {
            "file_path": output_path,
            "file_name": Path(output_path).name,
            "status": "completed",
        }
    except Exception as e:
        return {
            "file_path": None,
            "file_name": None,
            "status": "error",
            "error": str(e),
        }
