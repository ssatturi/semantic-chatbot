from datetime import datetime
from bson import ObjectId
from typing import Optional, List
from app.db.mongo_client import mongo_client
from app.utils.logger import logger

COLLECTION_NAME = "chat_messages"

async def save_message_metadata(data: dict) -> ObjectId:
    """
    Inserts a chat message into MongoDB and returns the inserted ObjectId.
    """
    try:
        db = mongo_client.get_db()
        document = {
            "from_user_id": data["from_user_id"],
            "to_user_id": data["to_user_id"],
            "message": data["message"],
            "timestamp": datetime.utcnow(),
            "session_id": data.get("session_id")  # Optional field
        }
        result = await db[COLLECTION_NAME].insert_one(document)
        logger.info("Message metadata saved", metadata_id=str(result.inserted_id))
        return result.inserted_id
    except Exception as e:
        logger.error("Failed to save message to MongoDB", error=str(e), data=data)
        raise

async def get_messages_by_user(user_id: str, direction: str = "all") -> List[dict]:
    """
    Retrieves messages involving a specific user:
    - direction = 'sent' returns messages from the user
    - direction = 'received' returns messages to the user
    - direction = 'all' returns both
    """
    try:
        db = mongo_client.get_db()
        if direction == "sent":
            query = {"from_user_id": user_id}
        elif direction == "received":
            query = {"to_user_id": user_id}
        else:
            query = {
                "$or": [
                    {"from_user_id": user_id},
                    {"to_user_id": user_id}
                ]
            }

        cursor = db[COLLECTION_NAME].find(query).sort("timestamp", 1)
        messages = await cursor.to_list(length=100)
        for m in messages:
            m["_id"] = str(m["_id"])
        logger.info("Fetched chat history", user_id=user_id, count=len(messages), direction=direction)
        return messages
    except Exception as e:
        logger.error("Failed to fetch messages", error=str(e), user_id=user_id)
        raise

async def delete_messages_by_user(user_id: str):
    """
    Deletes all messages sent by the specified user.
    """
    try:
        db = mongo_client.get_db()
        result = await db[COLLECTION_NAME].delete_many({"from_user_id": user_id})
        logger.info("Deleted messages from MongoDB", user_id=user_id, deleted=result.deleted_count)
    except Exception as e:
        logger.error("Failed to delete messages from MongoDB", error=str(e), user_id=user_id)
        raise
