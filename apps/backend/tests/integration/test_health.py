import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
async def client():
    """Cliente de teste assíncrono."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, client: AsyncClient):
        """Deve retornar status ok quando a API está saudável."""
        response = await client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "ok"
        assert "version" in data
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_health_returns_valid_version(self, client: AsyncClient):
        """Deve retornar versão no formato semântico."""
        response = await client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        version = data["version"]
        assert isinstance(version, str)
        # Versão deve seguir padrão semântico básico (ex: 0.1.0)
        parts = version.split(".")
        assert len(parts) >= 2
        assert all(part.isdigit() for part in parts[:2])

    @pytest.mark.asyncio
    async def test_health_timestamp_is_iso_format(self, client: AsyncClient):
        """Deve retornar timestamp em formato ISO."""
        response = await client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        timestamp = data["timestamp"]
        assert isinstance(timestamp, str)
        # Deve ser parseável como datetime ISO
        from datetime import datetime
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
