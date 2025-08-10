import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


@pytest.mark.asyncio
async def test_health_and_appointments_async():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        health = await ac.get("/health")
        assert health.status_code == 200
        assert health.json() == {"ok": True}

        apt = await ac.post(
            "/appointments",
            json={
                "name": "Charlie",
                "phone": "0698765432",
                "datetime": "2025-08-11T15:00:00Z",
            },
        )
        assert apt.status_code == 200
        assert apt.json()["received"]["name"] == "Charlie"
