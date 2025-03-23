from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.services.search_service import search_user_history
from app.utils.serialization import serialize_mongo_documents

router = APIRouter()

class SearchRequest(BaseModel):
    user_id: str = Field(..., example="user_A")
    query: str = Field(..., example="reset password")
    top_k: int = Field(5, ge=1, le=20)

@router.post("/search")
async def search_chat_history(payload: SearchRequest):
    """
    Semantic search endpoint using vector embeddings.
    Returns top-k semantically similar past messages for a given user.
    """
    try:
        results = await search_user_history(
            user_id=payload.user_id,
            query=payload.query,
            top_k=payload.top_k
        )
        serialized_results = serialize_mongo_documents(results)
        return {"status": "success", "results": serialized_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")
