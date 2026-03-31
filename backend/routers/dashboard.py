"""API de estatisticas para o dashboard."""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_session
from backend.models import Client

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session)):
    """Cards de resumo do dashboard."""
    result = await session.execute(select(Client))
    clients = result.scalars().all()

    total = len(clients)
    ativos = sum(1 for c in clients if c.status == "Ativa")
    encerrados = sum(1 for c in clients if c.status == "Encerrada")
    total_peticoes = sum(c.peticoes for c in clients)

    return {
        "total_clientes": total,
        "ativos": ativos,
        "encerrados": encerrados,
        "total_peticoes": total_peticoes,
    }


@router.get("/top-clients")
async def top_clients(
    limit: int = 15,
    session: AsyncSession = Depends(get_session),
):
    """Top N clientes por numero de peticoes."""
    result = await session.execute(
        select(Client).order_by(Client.peticoes.desc()).limit(limit)
    )
    clients = result.scalars().all()

    return [
        {"nome": c.nome, "peticoes": c.peticoes, "status": c.status}
        for c in clients
    ]


@router.get("/petition-types")
async def petition_types(session: AsyncSession = Depends(get_session)):
    """Distribuicao dos tipos de peticao (extraido da sintese)."""
    result = await session.execute(select(Client))
    clients = result.scalars().all()

    type_count = {}
    for c in clients:
        if not c.sintese:
            continue
        for part in c.sintese.split(";"):
            key = part.strip().split("(")[0].strip()
            if key and len(key) > 2:
                type_count[key] = type_count.get(key, 0) + 1

    sorted_types = sorted(type_count.items(), key=lambda x: x[1], reverse=True)[:15]
    return [{"tipo": t[0], "count": t[1]} for t in sorted_types]
