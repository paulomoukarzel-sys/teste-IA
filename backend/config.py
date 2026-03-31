"""Configuracoes do sistema."""

import os
from pathlib import Path

# Diretorios base
BASE_DIR = Path(__file__).resolve().parent.parent
CLIENTES_DIR = BASE_DIR / "Clientes"
DATA_DIR = BASE_DIR / "data"
SKILL_DIR = BASE_DIR / ".claude" / "skills" / "paulo-estilo-juridico"
FRONTEND_DIR = BASE_DIR / "frontend"

# Banco de dados
DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'juridico.db'}"

# Advogado padrao
ADVOGADO_NOME = "Paulo Ekke Moukarzel Junior"
ADVOGADO_OAB = "12345"
ADVOGADO_CIDADE = "Florianopolis"

# Servidor
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
