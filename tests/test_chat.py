import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_send_chat_message():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "from_user_id": "test_user_1",
            "to_user_id": "test_user_2",
            "message": "Is my invoice ready?",
            "session_id": "test_session"
        }
        response = await client.post("/api/chat", json=payload)
        assert response.status_code == 200
        assert "metadata_id" in response.json()["data"]
