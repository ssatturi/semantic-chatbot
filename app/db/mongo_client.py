from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import settings
from app.utils.logger import logger

class MongoDBClient:
    """
    MongoDB connector using Motor (async driver).
    Provides a shared DB instance for async operations.
    """

    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            logger.info("MongoDB client initialized", db_name=settings.MONGO_DB_NAME)
        except Exception as e:
            logger.error("Failed to initialize MongoDB client", error=str(e))
            raise

    def get_db(self):
        return self.db

# Singleton Mongo client for reuse
mongo_client = MongoDBClient()
