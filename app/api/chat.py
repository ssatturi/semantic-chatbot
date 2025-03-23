from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from app.services.chat_service import handle_incoming_message
from app.services.gdpr_service import request_user_data_deletion
from app.db.repository import get_messages_by_user

router = APIRouter()

class ChatMessage(BaseModel):
    from_user_id: str = Field(..., example="user_A")
    to_user_id: str = Field(..., example="user_B")
    message: str = Field(..., example="Hi there!")
    session_id: Optional[str] = Field(None, example="sess_123")

@router.post("/chat")
async def post_chat_message(payload: ChatMessage):
    try:
        result = await handle_incoming_message(payload.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message handling failed: {str(e)}")

@router.get("/chat/{user_id}")
async def get_chat_history(user_id: str, direction: str = Query("all", enum=["all", "sent", "received"])):
    try:
        messages = await get_messages_by_user(user_id, direction)
        return {"status": "success", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat history retrieval failed: {str(e)}")

@router.delete("/chat/{user_id}")
async def delete_user_data(user_id: str):
    try:
        result = await request_user_data_deletion(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GDPR deletion request failed: {str(e)}")
