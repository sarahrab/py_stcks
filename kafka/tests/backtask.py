import asyncio

from RequestsCRUD import RequestsCRUD


async def periodic_task(interval: int, crud: RequestsCRUD):
    try:
        while True:
            print("Task is running...")
            # Your task logic goes here
            await crud.check_requests()
            await asyncio.sleep(interval)  # Sleep asynchronously for interval seconds
    except asyncio.CancelledError:
        print("Periodic task has been cancelled.")
        raise

# Background task handler
async def run_background_tasks(requests: RequestsCRUD):
    task_interval = 5  # Task will run every 10 seconds
    task = asyncio.create_task(requests.periodic_check_requests(task_interval))  # Start the periodic task

    try:
        await asyncio.Future()  # Keep the event loop running indefinitely
    except asyncio.CancelledError:
        task.cancel()  # Cancel the periodic task gracefully
        await task  # Ensure proper cleanup
        raise

# # Run the periodic task on application startup
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(run_background_tasks())

# # Handle application shutdown gracefully
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Application is shutting down...")