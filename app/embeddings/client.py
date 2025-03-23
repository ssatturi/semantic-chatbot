from openai import OpenAI
from app.utils.config import settings
from app.utils.logger import logger

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding(text: str) -> list[float]:
    try:
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error("Failed to generate embedding", error=str(e))
        raise
