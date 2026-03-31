"""CRUD de clientes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.models import Client
from backend.services.client_service import sync_client_folders, list_client_files

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.get("")
async def list_clients(
    status: str | None = None,
    search: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """Lista clientes com filtros opcionais."""
    query = select(Client)

    if status:
        query = query.where(Client.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            Client.nome.ilike(search_term) | Client.sintese.ilike(search_term)
        )

    query = query.order_by(Client.nome)
    result = await session.execute(query)
    clients = result.scalars().all()

    return [
        {
            "id": c.id,
            "nome": c.nome,
            "status": c.status,
            "peticoes": c.peticoes,
            "tipos": c.tipos,
            "sintese": c.sintese,
            "folder_path": c.folder_path,
        }
        for c in clients
    ]


@router.get("/sync")
async def sync_folders(session: AsyncSession = Depends(get_session)):
    """Re-escaneia pastas em Clientes/ e atualiza folder_path."""
    await sync_client_folders(session)
    return {"status": "ok", "message": "Pastas sincronizadas."}


@router.get("/{client_id}")
async def get_client(client_id: int, session: AsyncSession = Depends(get_session)):
    """Detalhe de um cliente com stats."""
    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client:
        return {"error": "Cliente nao encontrado"}, 404

    return {
        "id": client.id,
        "nome": client.nome,
        "status": client.status,
        "peticoes": client.peticoes,
        "tipos": client.tipos,
        "sintese": client.sintese,
        "folder_path": client.folder_path,
    }


@router.post("")
async def create_client(data: dict, session: AsyncSession = Depends(get_session)):
    """Cria novo cliente."""
    client = Client(
        nome=data.get("nome", ""),
        status=data.get("status", "Ativa"),
        peticoes=data.get("peticoes", 0),
        tipos=data.get("tipos", 0),
        sintese=data.get("sintese", ""),
    )
    session.add(client)
    await session.commit()
    await session.refresh(client)
    return {"id": client.id, "nome": client.nome}


@router.put("/{client_id}")
async def update_client(
    client_id: int, data: dict, session: AsyncSession = Depends(get_session)
):
    """Atualiza dados de um cliente."""
    result = await session.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()

    if not client:
        return {"error": "Cliente nao encontrado"}, 404

    for field in ["nome", "status", "peticoes", "tipos", "sintese"]:
        if field in data:
            setattr(client, field, data[field])

    await session.commit()
    return {"id": client.id, "nome": client.nome, "status": "updated"}


@router.get("/{client_id}/documents")
async def client_documents(
    client_id: int, session: AsyncSession = Depends(get_session)
):
    """Documentos gerados para o cliente."""
    from backend.models import Document
    result = await session.execute(
        select(Document).where(Document.client_id == client_id).order_by(Document.created_at.desc())
    )
    docs = result.scalars().all()
    return [
        {
            "id": d.id,
            "titulo": d.titulo,
            "file_name": d.file_name,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


@router.get("/{client_id}/folder")
async def client_folder_files(
    client_id: int, session: AsyncSession = Depends(get_session)
):
    """Lista arquivos na pasta real do cliente."""
    files = await list_client_files(client_id, session)
    return files
