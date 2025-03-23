from app.embeddings.client import get_embedding
from app.db.qdrant_client import qdrant
from app.db.mongo_client import mongo_client
from bson import ObjectId
from app.utils.logger import logger
from typing import List

async def search_user_history(user_id: str, query: str, top_k: int = 5) -> List[dict]:
    """
    Semantic search flow:
    1. Embed the query using OpenAI
    2. Search Qdrant vectors scoped to user_id
    3. Fetch full message metadata from MongoDB
    """
    try:
        logger.info("Semantic search initiated", user_id=user_id, query=query, top_k=top_k)

        # Step 1: Generate query embedding
        query_vector = get_embedding(query)

        # Step 2: Perform vector search
        results = qdrant.search(user_id=user_id, query_vector=query_vector, top_k=top_k)
        metadata_ids = [r.payload.get("metadata_id") for r in results if "metadata_id" in r.payload]

        if not metadata_ids:
            logger.info("No matches found in vector search", user_id=user_id)
            return []

        # Step 3: Fetch metadata from MongoDB
        db = mongo_client.get_db()
        cursor = db["chat_messages"].find({"_id": {"$in": [ObjectId(mid) for mid in metadata_ids]}})
        messages = await cursor.to_list(length=top_k)

        logger.info("Semantic search complete", user_id=user_id, hits=len(messages))
        return messages

    except Exception as e:
        logger.error("Semantic search failed", error=str(e), user_id=user_id)
        raise
