"""Geracao e download de documentos .docx."""

from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.models import Document, Client
from backend.services.document_service import generate_docx

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/generate")
async def generate_document(
    data: dict, session: AsyncSession = Depends(get_session)
):
    """Dispara geracao de .docx."""
    client_id = data.get("client_id")
    conversation_id = data.get("conversation_id")
    titulo = data.get("titulo", "PETICAO")
    conteudo = data.get("conteudo", "")
    cliente_nome = data.get("cliente_nome", "")

    # Buscar nome do cliente se nao fornecido
    if client_id and not cliente_nome:
        result = await session.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        if client:
            cliente_nome = client.nome

    if not conteudo.strip():
        return {"error": "Conteudo vazio"}, 400

    # Criar registro do documento
    doc = Document(
        client_id=client_id,
        conversation_id=conversation_id,
        titulo=titulo,
        status="generating",
        content_text=conteudo,
    )
    session.add(doc)
    await session.commit()
    await session.refresh(doc)

    # Gerar .docx
    result = await generate_docx(
        titulo=titulo,
        conteudo=conteudo,
        cliente=cliente_nome,
    )

    doc.status = result["status"]
    doc.file_path = result.get("file_path")
    doc.file_name = result.get("file_name")
    await session.commit()

    return {
        "id": doc.id,
        "status": doc.status,
        "file_name": doc.file_name,
        "file_path": doc.file_path,
        "error": result.get("error"),
    }


@router.get("/{doc_id}")
async def get_document(doc_id: int, session: AsyncSession = Depends(get_session)):
    """Metadados de um documento."""
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        return {"error": "Documento nao encontrado"}, 404

    return {
        "id": doc.id,
        "titulo": doc.titulo,
        "file_name": doc.file_name,
        "file_path": doc.file_path,
        "status": doc.status,
        "created_at": doc.created_at.isoformat() if doc.created_at else None,
    }


@router.get("/{doc_id}/download")
async def download_document(
    doc_id: int, session: AsyncSession = Depends(get_session)
):
    """Download do arquivo .docx."""
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc or not doc.file_path:
        return {"error": "Documento nao encontrado"}, 404

    file_path = Path(doc.file_path)
    if not file_path.exists():
        return {"error": "Arquivo nao encontrado no disco"}, 404

    return FileResponse(
        path=str(file_path),
        filename=doc.file_name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/{doc_id}/preview")
async def preview_document(
    doc_id: int, session: AsyncSession = Depends(get_session)
):
    """Texto do documento para preview."""
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        return {"error": "Documento nao encontrado"}, 404

    return {
        "id": doc.id,
        "titulo": doc.titulo,
        "content_text": doc.content_text or "",
        "status": doc.status,
    }
