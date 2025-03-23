from app.db.mongo_client import mongo_client
from app.db.qdrant_client import qdrant
from app.queue.kafka_queue import gdpr_queue  # Or swap with in_memory
from app.utils.logger import logger

async def process_gdpr_queue():
    """
    Background worker that continuously checks the deletion queue.
    Deletes user data from both MongoDB and Qdrant.
    """
    db = mongo_client.get_db()

    while True:
        user_id = await gdpr_queue.dequeue()
        if user_id is None:
            break  # No more items in queue

        try:
            # Step 1: Delete from MongoDB
            result = await db["chat_messages"].delete_many({"from_user_id": user_id})
            logger.info("Deleted messages from MongoDB", user_id=user_id, deleted_count=result.deleted_count)

            # Step 2: Delete from Qdrant
            qdrant.delete_vectors_by_user(user_id)
            logger.info("Deleted vectors from Qdrant", user_id=user_id)

        except Exception as e:
            logger.error("GDPR worker failed for user", user_id=user_id, error=str(e))
# GDPR deletion worker
