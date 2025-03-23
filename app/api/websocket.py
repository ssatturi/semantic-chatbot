from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.logger import logger

router = APIRouter()

# In-memory user_id → WebSocket map
active_connections: dict[str, WebSocket] = {}

@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    logger.info("WebSocket connected", user_id=user_id)

    try:
        while True:
            await websocket.receive_text()  # Keeps the connection alive
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
        logger.info("WebSocket disconnected", user_id=user_id)

def send_message_to_user(user_id: str, message_data: dict):
    """
    Sends a message to a user via WebSocket if they are connected.
    """
    websocket = active_connections.get(user_id)
    if websocket:
        try:
            import asyncio
            asyncio.create_task(websocket.send_json(message_data))
            logger.info("Real-time message sent", to_user=user_id, message=message_data)
        except Exception as e:
            logger.error("WebSocket message send failed", user_id=user_id, error=str(e))
