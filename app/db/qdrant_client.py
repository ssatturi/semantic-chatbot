from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from app.utils.config import settings
from app.utils.logger import logger
import uuid

class QdrantVectorStore:
    """
    Handles interaction with Qdrant vector database.
    Supports insert, search, and delete operations.
    """

    def __init__(self):
        try:
            self.client = QdrantClient(url=settings.QDRANT_HOST)
            self.collection = settings.QDRANT_COLLECTION
            self._init_collection()
            logger.info("Qdrant client initialized", host=settings.QDRANT_HOST, collection=self.collection)
        except Exception as e:
            logger.error("Failed to initialize Qdrant client", error=str(e))
            raise

    def _init_collection(self):
        """Create collection if it does not exist."""
        existing = self.client.get_collections().collections
        if self.collection not in [c.name for c in existing]:
            self.client.recreate_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIM,
                    distance=Distance.COSINE
                )
            )
            logger.info("Qdrant collection created", collection=self.collection)

    def insert_vector(self, user_id: str, embedding: list[float], metadata_id: str):
        """Insert a single vector with metadata into the Qdrant collection."""
        try:
            self.client.upsert(
                collection_name=self.collection,
                points=[
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "user_id": user_id,
                            "metadata_id": metadata_id
                        }
                    )
                ]
            )
            logger.info("Inserted vector to Qdrant", user_id=user_id, metadata_id=metadata_id)
        except Exception as e:
            logger.error("Qdrant vector insert failed", error=str(e), user_id=user_id)

    def search(self, user_id: str, query_vector: list[float], top_k: int = 5):
        """Search vectors by user filter and return top_k similar results."""
        try:
            results = self.client.search(
                collection_name=self.collection,
                query_vector=query_vector,
                limit=top_k,
                query_filter=Filter(
                    must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
                )
            )
            logger.info("Qdrant search completed", user_id=user_id, top_k=top_k, hits=len(results))
            return results
        except Exception as e:
            logger.error("Qdrant search failed", error=str(e), user_id=user_id)
            return []

    def delete_vectors_by_user(self, user_id: str):
        """Delete all vectors associated with a specific user."""
        try:
            self.client.delete(
                collection_name=self.collection,
                filter=Filter(
                    must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
                )
            )
            logger.info("Qdrant vectors deleted for user", user_id=user_id)
        except Exception as e:
            logger.error("Qdrant vector deletion failed", error=str(e), user_id=user_id)

# Singleton instance
qdrant = QdrantVectorStore()
