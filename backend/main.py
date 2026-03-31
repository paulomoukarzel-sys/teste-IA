"""FastAPI application principal."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import FRONTEND_DIR, BASE_DIR
from backend.database import init_db
from backend.migrations.seed_clients import seed
from backend.routers import clients, conversations, documents, dashboard, ws_chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: cria DB e faz seed."""
    await init_db()
    await seed()
    yield


app = FastAPI(
    title="Assistente Juridico - Dr. Paulo Moukarzel",
    version="1.0.0",
    lifespan=lifespan,
)

# Routers
app.include_router(clients.router)
app.include_router(conversations.router)
app.include_router(documents.router)
app.include_router(dashboard.router)
app.include_router(ws_chat.router)

# Servir arquivos estaticos do frontend
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")


@app.get("/")
async def serve_index():
    """Serve a pagina principal do chat."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/dashboard")
async def serve_dashboard():
    """Serve o dashboard existente."""
    return FileResponse(str(BASE_DIR / "dashboard_clientes.html"))
