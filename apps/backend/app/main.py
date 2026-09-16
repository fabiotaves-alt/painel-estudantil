import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime

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

    # CORS restrito (apenas Tauri em desenvolvimento)
    if settings.debug:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "tauri://localhost"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            allow_headers=["Content-Type", settings.api_token_header],
        )

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
                    "timestamp": datetime.utcnow().isoformat(),
                },
            },
        )

    # Incluir router principal
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
