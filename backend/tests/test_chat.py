# app/tests/test_chat.py
import pytest
from httpx import AsyncClient
from app.main import create_app

app = create_app()

@pytest.mark.asyncio
async def test_alive():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/_alive")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
