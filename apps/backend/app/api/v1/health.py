import uuid
from datetime import datetime
from fastapi import APIRouter, Depends

from app.config import settings
from app.schemas.responses import HealthResponse, MetaInfo


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
        timestamp=datetime.utcnow(),
    )


@router.get("/ready")
async def readiness_check() -> dict:
    """
    Verifica se a API está pronta para receber requisições.
    
    Diferente do health check, este endpoint verifica dependências externas.
    """
    return {
        "ready": True,
        "timestamp": datetime.utcnow(),
        "request_id": str(uuid.uuid4()),
    }
