from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.queue.base import BaseQueue
from app.utils.config import settings
from app.utils.logger import logger
import asyncio

class KafkaQueue(BaseQueue):
    """
    Kafka-based implementation of BaseQueue for production message processing.
    Uses aiokafka for async publish/consume.
    """

    def __init__(self):
        self.topic = settings.KAFKA_TOPIC
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.group_id = settings.KAFKA_GROUP_ID
        self._producer = None
        self._consumer = None
        self._loop = asyncio.get_event_loop()

    async def _init_producer(self):
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers
            )
            await self._producer.start()
            logger.info("Kafka producer initialized")

    async def _init_consumer(self):
        if not self._consumer:
            self._consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset="earliest",
                enable_auto_commit=True
            )
            await self._consumer.start()
            logger.info("Kafka consumer initialized", topic=self.topic)

    async def enqueue(self, item: str) -> None:
        await self._init_producer()
        await self._producer.send_and_wait(self.topic, item.encode("utf-8"))
        logger.info("Enqueued item to Kafka", item=item)

    async def dequeue(self) -> str | None:
        await self._init_consumer()
        try:
            msg = await self._consumer.getone()
            decoded = msg.value.decode("utf-8")
            logger.info("Dequeued item from Kafka", item=decoded)
            return decoded
        except Exception as e:
            logger.error("Kafka dequeue error", error=str(e))
            return None

    def length(self) -> int:
        logger.warning("KafkaQueue.length() not supported")
        return -1  # Kafka doesn't expose queue length synchronously

# Export instance
gdpr_queue = KafkaQueue()
