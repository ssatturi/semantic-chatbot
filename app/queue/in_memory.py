from collections import deque
from typing import Optional
from app.queue.base import BaseQueue
from app.utils.logger import logger

class InMemoryQueue(BaseQueue):
    """
    Simple in-memory queue for development/testing.
    Can be swapped with Kafka or Redis without changing service logic.
    """

    def __init__(self):
        self._queue = deque()

    async def enqueue(self, item: str) -> None:
        self._queue.append(item)
        logger.info("Enqueued item to in-memory queue", item=item, queue_size=self.length())

    async def dequeue(self) -> Optional[str]:
        if self._queue:
            item = self._queue.popleft()
            logger.info("Dequeued item from in-memory queue", item=item, remaining=self.length())
            return item
        return None

    def length(self) -> int:
        return len(self._queue)

# Singleton instance
gdpr_queue = InMemoryQueue()
# In-memory queue implementation
