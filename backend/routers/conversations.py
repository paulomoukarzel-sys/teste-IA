"""Gestao de conversas."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.models import Conversation, Message

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("")
async def list_conversations(
    client_id: int | None = None,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    """Lista conversas, opcionalmente filtradas por cliente."""
    query = select(Conversation).order_by(Conversation.updated_at.desc())

    if client_id is not None:
        query = query.where(Conversation.client_id == client_id)

    query = query.offset(offset).limit(limit)
    result = await session.execute(query)
    convs = result.scalars().all()

    return [
        {
            "id": c.id,
            "client_id": c.client_id,
            "title": c.title,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in convs
    ]


@router.post("")
async def create_conversation(
    data: dict, session: AsyncSession = Depends(get_session)
):
    """Cria nova conversa."""
    conv = Conversation(
        client_id=data.get("client_id"),
        title=data.get("title", "Nova conversa"),
    )
    session.add(conv)
    await session.commit()
    await session.refresh(conv)
    return {"id": conv.id, "title": conv.title}


@router.get("/{conv_id}")
async def get_conversation(
    conv_id: int, session: AsyncSession = Depends(get_session)
):
    """Retorna conversa com todas as mensagens."""
    result = await session.execute(
        select(Conversation).where(Conversation.id == conv_id)
    )
    conv = result.scalar_one_or_none()

    if not conv:
        return {"error": "Conversa nao encontrada"}, 404

    msg_result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at)
    )
    messages = msg_result.scalars().all()

    return {
        "id": conv.id,
        "client_id": conv.client_id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "message_type": m.message_type,
                "content": m.content,
                "metadata_json": m.metadata_json,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
    }


@router.delete("/{conv_id}")
async def delete_conversation(
    conv_id: int, session: AsyncSession = Depends(get_session)
):
    """Remove conversa e suas mensagens."""
    result = await session.execute(
        select(Conversation).where(Conversation.id == conv_id)
    )
    conv = result.scalar_one_or_none()

    if not conv:
        return {"error": "Conversa nao encontrada"}, 404

    # Deletar mensagens
    msg_result = await session.execute(
        select(Message).where(Message.conversation_id == conv_id)
    )
    for msg in msg_result.scalars().all():
        await session.delete(msg)

    await session.delete(conv)
    await session.commit()
    return {"status": "deleted"}
