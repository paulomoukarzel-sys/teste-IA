"""Integracao com Claude via CLI (usa assinatura existente do Claude Code)."""

import asyncio
import json
import os
from typing import AsyncGenerator
from backend.services.skill_loader import load_system_prompt, get_client_context


def _build_env() -> dict:
    """Prepara environment para subprocess do claude CLI."""
    env = os.environ.copy()
    # Remover CLAUDECODE para permitir execucao nested
    env.pop("CLAUDECODE", None)
    return env


async def stream_response(
    messages: list[dict],
    client_info: dict | None = None,
) -> AsyncGenerator[str, None]:
    """
    Envia mensagens para o Claude via CLI e faz streaming da resposta.

    Usa 'claude -p --output-format stream-json' para streaming token por token,
    aproveitando a assinatura existente do Claude Code (sem API key separada).
    """
    system_prompt = load_system_prompt()

    if client_info:
        system_prompt += get_client_context(
            client_nome=client_info.get("nome", ""),
            client_status=client_info.get("status", "Ativa"),
            client_peticoes=client_info.get("peticoes", 0),
            client_sintese=client_info.get("sintese", ""),
        )

    # Montar o prompt final: system prompt + historico + ultima mensagem
    prompt_parts = [system_prompt, "\n\n---\n\n"]

    # Adicionar historico de mensagens como contexto
    for msg in messages[:-1]:  # Todas exceto a ultima
        role_label = "Usuario" if msg["role"] == "user" else "Assistente"
        prompt_parts.append(f"[{role_label}]: {msg['content']}\n\n")

    # Ultima mensagem do usuario
    if messages:
        last_msg = messages[-1]
        prompt_parts.append(last_msg["content"])

    full_prompt = "".join(prompt_parts)

    env = _build_env()

    # Executar claude CLI com streaming JSON
    process = await asyncio.create_subprocess_exec(
        "claude", "-p",
        "--output-format", "stream-json",
        "--max-turns", "1",
        "--no-input",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    # Enviar prompt via stdin
    process.stdin.write(full_prompt.encode("utf-8"))
    await process.stdin.drain()
    process.stdin.close()

    # Ler streaming linha por linha
    has_streamed = False
    buffer = b""
    while True:
        chunk = await process.stdout.read(4096)
        if not chunk:
            break

        buffer += chunk
        lines = buffer.split(b"\n")
        buffer = lines[-1]  # Manter resto incompleto no buffer

        for line in lines[:-1]:
            line = line.strip()
            if not line:
                continue

            try:
                event = json.loads(line)
                event_type = event.get("type", "")

                if event_type == "content_block_delta":
                    delta = event.get("delta", {})
                    text = delta.get("text", "")
                    if text:
                        has_streamed = True
                        yield text

                elif event_type == "assistant" and "message" in event:
                    content = event["message"]
                    if content and not has_streamed:
                        has_streamed = True
                        yield content

                elif event_type == "result":
                    result_text = event.get("result", "")
                    if result_text and not has_streamed:
                        has_streamed = True
                        yield result_text

            except json.JSONDecodeError:
                continue

    # Processar ultimo pedaco do buffer
    if buffer.strip():
        try:
            event = json.loads(buffer)
            event_type = event.get("type", "")

            if event_type == "content_block_delta":
                delta = event.get("delta", {})
                text = delta.get("text", "")
                if text:
                    has_streamed = True
                    yield text

            elif event_type == "result":
                result_text = event.get("result", "")
                if result_text and not has_streamed:
                    has_streamed = True
                    yield result_text

        except json.JSONDecodeError:
            pass

    await process.wait()

    # Se o processo falhou, verificar stderr
    if process.returncode and process.returncode != 0:
        stderr = await process.stderr.read()
        error_msg = stderr.decode("utf-8", errors="replace").strip()
        if error_msg:
            yield f"\n\n[Erro do Claude CLI: {error_msg}]"
    elif not has_streamed:
        yield "[Nenhuma resposta recebida do Claude CLI]"


async def single_response(
    messages: list[dict],
    client_info: dict | None = None,
) -> str:
    """Envia mensagens e retorna resposta completa (sem streaming)."""
    full_text = []
    async for token in stream_response(messages, client_info):
        full_text.append(token)
    return "".join(full_text)
