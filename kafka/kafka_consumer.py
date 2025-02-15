import asyncio
from typing import List

from aiokafka import AIOKafkaConsumer


class KafkaConsumerClient:
    massages: List[str]

    def __init__(self, topic, group_id="client_group", bootstrap_servers="localhost:9092"):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",  # Consume from the earliest messages if none are consumed yet
            enable_auto_commit=False  # Disable auto-commit for manual offset management
        )
        self.task = None  # To keep track of background task (for consuming messages)

    async def start(self):
        """Starts consuming messages asynchronously."""
        await self.consumer.start()
        print(f"Kafka Consumer for topic '{self.topic}' started.")
        self.task = asyncio.create_task(self._consume_messages())

    async def _consume_messages(self):
        """The method to consume messages asynchronously."""
        try:
            async for msg in self.consumer:
                message = msg.value.decode()
                self.massages.append(message)
                #print(f"Received message: {msg.value.decode()} (offset: {msg.offset}, partition: {msg.partition})")

                # Manual offset commit after processing the message
                await self.consumer.commit()
        except Exception as e:
            print(f"Consumer error: {e}")
        finally:
            print("Consumer stopped consuming.")

    async def stop(self):
        """Stops consuming messages."""
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass  # Task was canceled without issues
        await self.consumer.stop()
        print(f"Kafka Consumer for topic '{self.topic}' stopped.")

    async def consume_for_duration(self, duration=30):
        """Consume messages for a specified duration (e.g., 30 seconds)."""
        await self.start()
        await asyncio.sleep(duration)  # Keep consuming for the specified time
        await self.stop()



