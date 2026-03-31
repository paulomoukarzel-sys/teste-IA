"""Servico de clientes: scan de pastas e sync de dados."""

import os
import unicodedata
import re
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import CLIENTES_DIR
from backend.models import Client


def _normalize_name(name: str) -> str:
    """Remove acentos e normaliza para comparacao."""
    nfkd = unicodedata.normalize('NFKD', name)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def _find_client_folder(client_nome: str) -> str | None:
    """Tenta encontrar a pasta real do cliente em Clientes/."""
    if not CLIENTES_DIR.exists():
        return None

    normalized = _normalize_name(client_nome)
    # Remover sufixos entre parenteses para match
    base_name = re.sub(r'\s*\(.*?\)\s*', ' ', normalized).strip()

    # Buscar em todas as subpastas (ativas e encerradas)
    for root_dir in [CLIENTES_DIR, CLIENTES_DIR / "01 - Atuações encerradas"]:
        if not root_dir.exists():
            continue
        for entry in root_dir.iterdir():
            if entry.is_dir():
                entry_normalized = _normalize_name(entry.name)
                if (entry_normalized == normalized or
                    entry_normalized == base_name or
                    base_name in entry_normalized or
                    entry_normalized in base_name):
                    return str(entry)

    return None


async def sync_client_folders(session: AsyncSession):
    """Atualiza folder_path de todos os clientes com base no scan de Clientes/."""
    result = await session.execute(select(Client))
    clients = result.scalars().all()

    for client in clients:
        if not client.folder_path:
            folder = _find_client_folder(client.nome)
            if folder:
                client.folder_path = folder

    await session.commit()


async def list_client_files(client_id: int, session: AsyncSession) -> list[dict]:
    """Lista arquivos na pasta real do cliente."""
    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client or not client.folder_path:
        return []

    folder = Path(client.folder_path)
    if not folder.exists():
        return []

    files = []
    for item in sorted(folder.rglob("*")):
        if item.is_file():
            files.append({
                "name": item.name,
                "path": str(item),
                "size": item.stat().st_size,
                "relative_path": str(item.relative_to(folder)),
            })

    return files
