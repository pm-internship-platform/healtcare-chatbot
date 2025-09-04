# app/tests/test_health.py
import pytest
from httpx import AsyncClient
from app.main import create_app

app = create_app()

@pytest.mark.asyncio
async def test_health_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/health/status")
        assert r.status_code == 200
        assert "info" in r.json()
