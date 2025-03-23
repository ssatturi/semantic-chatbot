from pydantic_settings import BaseSettings
from pydantic import Field
from pymongo import MongoClient
from qdrant_client import QdrantClient


class Settings(BaseSettings):
    # === MongoDB ===
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB_NAME: str = Field(..., env="MONGO_DB_NAME")

    # === Qdrant ===
    QDRANT_HOST: str = Field(..., env="QDRANT_HOST")
    QDRANT_COLLECTION: str = Field(..., env="QDRANT_COLLECTION")
    EMBEDDING_DIM: int = Field(..., env="EMBEDDING_DIM")

    # === OpenAI ===
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = Field(..., env="OPENAI_EMBEDDING_MODEL")

    # === Kafka ===
    KAFKA_BOOTSTRAP_SERVERS: str = Field(..., env="KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC: str = Field(..., env="KAFKA_TOPIC")
    KAFKA_GROUP_ID: str = Field(..., env="KAFKA_GROUP_ID")

    # === OpenTelemetry ===
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(..., env="OTEL_EXPORTER_OTLP_ENDPOINT")
    DEBUG: bool = Field(default=False, env="DEBUG")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # ✅ allows extra env vars    #

    # # === Helpers ===
    # def get_mongo_client(self) -> MongoClient:
    #     return MongoClient(self.MONGO_URI)
    #
    # def get_qdrant_client(self) -> QdrantClient:
    #     return QdrantClient(url=self.QDRANT_HOST)


# ✅ Global settings instance
settings = Settings()
