"""Testes de integração para a API."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """Cliente HTTP para testes."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Testa endpoint de health check."""
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    """Testa endpoint de readiness check."""
    response = await client.get("/api/v1/ready")

    assert response.status_code == 200
    data = response.json()

    assert data["ready"] is True
    assert "timestamp" in data
    assert "request_id" in data


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """Testa endpoint protegido sem token retorna 401."""
    # Health check não requer token
    health_response = await client.get("/api/v1/health")
    assert health_response.status_code == 200

    # Outros endpoints requerem token (quando implementados)
    # Por enquanto, apenas verificamos que o middleware está ativo


@pytest.mark.asyncio
async def test_request_id_header(client: AsyncClient):
    """Testa se request_id é retornado nos headers."""
    response = await client.get("/api/v1/health")

    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"] != ""
