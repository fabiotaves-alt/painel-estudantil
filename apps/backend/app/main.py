import logging
import secrets
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.infrastructure.database import database

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação."""
    # Startup
    logger.info("Iniciando aplicação %s v%s", settings.app_name, settings.app_version)

    # Inicializar banco de dados
    database.init()
    await database.create_tables()
    logger.info("Banco de dados inicializado")

    yield

    # Shutdown
    logger.info("Encerrando aplicação")
    
    # Fechar conexões do banco de dados
    await database.dispose()
    logger.info("Conexões do banco de dados fechadas")


def create_app() -> FastAPI:
    """Factory para criar a aplicação FastAPI."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API para Dashboard Acadêmico Offline-First",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # Armazenar token no estado da aplicação em vez de variável global
    app.state.execution_token = secrets.token_urlsafe(32)
    logger.info("Token de execução gerado (não logar)")

    # CORS restrito (apenas origem Tauri)
    if settings.debug:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # Vite dev server
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            allow_headers=[
                "Content-Type",
                "Authorization",
                settings.api_token_header,
                "X-Request-ID",
            ],
        )

    # Middleware para autenticação por token (exceto health check)
    @app.middleware("http")
    async def verify_token(request: Request, call_next):
        # Health check não requer token
        if request.url.path in ["/api/v1/health", "/api/v1/ready"]:
            return await call_next(request)

        # Verificar token de execução usando app.state em vez de variável global
        token = request.headers.get(settings.api_token_header)
        current_token = getattr(request.app.state, "execution_token", None)

        if not token or not secrets.compare_digest(token, current_token):
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Token de autenticação inválido ou ausente",
                        "details": None,
                    },
                    "meta": {
                        "request_id": str(uuid.uuid4()),
                        "timestamp": datetime.now(UTC).isoformat(),
                    },
                },
            )

        return await call_next(request)

    # Middleware para logging e request_id
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    # Handler global de erros
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("Erro não tratado: %s", exc, exc_info=exc)

        if settings.debug:
            message = str(exc)
        else:
            message = "Erro interno do servidor"

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": message,
                    "details": None,
                },
                "meta": {
                    "request_id": request.headers.get("x-request-id", "unknown"),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            },
        )

    # Incluir router principal
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dashboard Acadêmico Backend")
    parser.add_argument("--port", type=int, default=settings.port, help="Porta do servidor")
    parser.add_argument("--host", type=str, default=settings.host, help="Host do servidor")
    args = parser.parse_args()

    # Sobrescrever configurações com argumentos de linha de comando
    settings.host = args.host
    settings.port = args.port

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=settings.debug,
    )
