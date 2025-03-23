from app.queue.kafka_queue import gdpr_queue  # Swapable for in_memory if needed
from app.utils.logger import logger
from app.events import GDPRDeletionEvent
from datetime import datetime
import uuid


async def request_user_data_deletion(user_id: str) -> dict:
    """
    Handles GDPR deletion request.
    Publishes the user_id to the deletion queue.
    Actual deletion is handled by a background worker.
    """
    try:
        await gdpr_queue.enqueue(user_id)
        logger.info("GDPR deletion request enqueued", user_id=user_id)
        return {
            "status": "queued",
            "message": f"User data deletion for '{user_id}' has been accepted for processing."
        }
    except Exception as e:
        logger.error("Failed to enqueue GDPR deletion", error=str(e), user_id=user_id)
        raise
