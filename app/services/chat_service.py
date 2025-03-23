from app.embeddings.client import get_embedding
from app.db.repository import save_message_metadata
from app.db.qdrant_client import qdrant
from app.api.websocket import send_message_to_user
from app.utils.logger import logger

async def handle_incoming_message(data: dict) -> dict:
    """
    Handles a new incoming chat message:
    1. Generate vector embedding from the message
    2. Save structured metadata to MongoDB
    3. Store vector in Qdrant
    4. Optionally send real-time message via WebSocket
    Returns the MongoDB metadata ID
    """
    from_user = data["from_user_id"]
    to_user = data["to_user_id"]
    message = data["message"]

    try:
        logger.info("Handling incoming chat message", from_user=from_user, to_user=to_user)

        # Step 1: Embed message using OpenAI
        embedding = get_embedding(message)
        logger.info("Embedding generated", dimensions=len(embedding))

        # Step 2: Store metadata in MongoDB
        metadata_id = await save_message_metadata(data)
        logger.info("Chat metadata saved", metadata_id=str(metadata_id))

        # Step 3: Store vector in Qdrant
        qdrant.insert_vector(user_id=from_user, embedding=embedding, metadata_id=str(metadata_id))
        logger.info("Vector stored in Qdrant", user_id=from_user)

        # Step 4: Send message via WebSocket to recipient if connected
        send_message_to_user(
            user_id=to_user,
            message_data={
                "from": from_user,
                "message": message,
                "metadata_id": str(metadata_id)
            }
        )

        return {"metadata_id": str(metadata_id)}

    except Exception as e:
        logger.error("Failed to process chat message", error=str(e), from_user=from_user)
        raise
