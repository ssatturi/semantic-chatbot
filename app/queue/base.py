from abc import ABC, abstractmethod
from typing import Optional

class BaseQueue(ABC):
    """
    Abstract base class for pluggable message queues.
    Used for async tasks like GDPR deletion.
    """

    @abstractmethod
    async def enqueue(self, item: str) -> None:
        """Add a task to the queue."""
        pass

    @abstractmethod
    async def dequeue(self) -> Optional[str]:
        """Retrieve and remove the next task from the queue."""
        pass

    @abstractmethod
    def length(self) -> int:
        """Returns the number of items in the queue."""
        pass
# Abstract queue interface
