import uuid
from datetime import UTC, datetime

from fastapi import APIRouter

from app.config import settings
from app.infrastructure.database import database
from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Verifica se a API está saudável.

    Retorna status 'ok' se o serviço estiver operacional.
    Este endpoint não requer autenticação.
    """
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        timestamp=datetime.now(UTC),
    )


@router.get("/ready")
async def readiness_check() -> dict:
    """
    Verifica se a API está pronta para receber requisições.

    Diferente do health check, este endpoint verifica dependências externas.
    """
    # Verificar conexão com banco de dados
    try:
        await database.engine.connect()
        db_status = "connected"
        ready = True
    except Exception as e:
        db_status = f"error: {str(e)}"
        ready = False
    
    return {
        "ready": ready,
        "database": db_status,
        "timestamp": datetime.now(UTC).isoformat(),
        "request_id": str(uuid.uuid4()),
    }
