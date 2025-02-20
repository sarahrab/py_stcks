import asyncio
from aiokafka import AIOKafkaConsumer

async def consume_messages(consumer: AIOKafkaConsumer):
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message: {msg.value.decode()}")
    finally:
        await consumer.stop()

async def run_client():
    # Your client logic here. For example, just an infinite loop.
    while True:
        await asyncio.sleep(1)
        print("Client running...")  # You can add your actual client logic here.

async def main():
    # Configure the Kafka consumer
    consumer = AIOKafkaConsumer(
        'your_topic',  # Replace with your topic name
        loop=asyncio.get_event_loop(),
        bootstrap_servers='your_kafka_broker',  # Replace with your Kafka broker address
        group_id='your_consumer_group',  # Replace with your consumer group
    )

    # Run both the consumer and the client in the background
    await asyncio.gather(
        consume_messages(consumer),  # Start the consumer in the background
        run_client()  # Start your main client
    )

if __name__ == "__main__":
    # Run the event loop
    asyncio.run(main())