"""WebSocket handler para chat com streaming."""

import json
import traceback
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from backend.database import async_session
from backend.models import Conversation, Message, Client
from backend.services.claude_service import stream_response

router = APIRouter()


@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: int):
    """Chat WebSocket com streaming de resposta da IA."""
    await websocket.accept()

    try:
        while True:
            # Receber mensagem do usuario
            raw = await websocket.receive_text()
            data = json.loads(raw)
            user_content = data.get("content", "")
            message_type = data.get("message_type", "text")
            metadata = data.get("metadata", None)

            if not user_content.strip():
                continue

            async with async_session() as session:
                # Verificar se a conversa existe
                result = await session.execute(
                    select(Conversation).where(Conversation.id == conversation_id)
                )
                conv = result.scalar_one_or_none()

                if not conv:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "content": "Conversa nao encontrada."
                    }))
                    continue

                # Auto-gerar titulo da conversa a partir da primeira mensagem
                msg_count_result = await session.execute(
                    select(Message).where(Message.conversation_id == conversation_id)
                )
                existing_msgs = msg_count_result.scalars().all()
                if not existing_msgs:
                    conv.title = user_content[:80] + ("..." if len(user_content) > 80 else "")

                # Salvar mensagem do usuario
                user_msg = Message(
                    conversation_id=conversation_id,
                    role="user",
                    message_type=message_type,
                    content=user_content,
                    metadata_json=metadata,
                )
                session.add(user_msg)
                await session.commit()

                # Confirmar recebimento
                await websocket.send_text(json.dumps({
                    "type": "user_message_saved",
                    "message_id": user_msg.id,
                }))

                # Montar historico de mensagens para a API
                msg_result = await session.execute(
                    select(Message)
                    .where(Message.conversation_id == conversation_id)
                    .where(Message.role.in_(["user", "assistant"]))
                    .order_by(Message.created_at)
                )
                history = msg_result.scalars().all()

                api_messages = []
                for msg in history:
                    api_messages.append({
                        "role": msg.role,
                        "content": msg.content,
                    })

                # Buscar info do cliente (se associado)
                client_info = None
                if conv.client_id:
                    client_result = await session.execute(
                        select(Client).where(Client.id == conv.client_id)
                    )
                    client = client_result.scalar_one_or_none()
                    if client:
                        client_info = {
                            "nome": client.nome,
                            "status": client.status,
                            "peticoes": client.peticoes,
                            "sintese": client.sintese,
                        }

                # Indicar inicio do streaming
                await websocket.send_text(json.dumps({
                    "type": "stream_start",
                }))

                # Fazer streaming da resposta
                full_response = []
                try:
                    async for token in stream_response(api_messages, client_info):
                        full_response.append(token)
                        await websocket.send_text(json.dumps({
                            "type": "stream_token",
                            "content": token,
                        }))
                except Exception as e:
                    error_msg = f"Erro na API Claude: {str(e)}"
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "content": error_msg,
                    }))
                    full_response = [error_msg]

                # Salvar resposta completa
                assistant_content = "".join(full_response)
                assistant_msg = Message(
                    conversation_id=conversation_id,
                    role="assistant",
                    message_type="text",
                    content=assistant_content,
                )
                session.add(assistant_msg)
                conv.updated_at = datetime.now(timezone.utc)
                await session.commit()

                # Indicar fim do streaming
                await websocket.send_text(json.dumps({
                    "type": "stream_end",
                    "message_id": assistant_msg.id,
                    "full_content": assistant_content,
                }))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": f"Erro interno: {str(e)}",
            }))
        except Exception:
            pass
