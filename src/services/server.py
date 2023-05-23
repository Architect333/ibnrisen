import asyncio
import uvicorn
from src.services.api import AppSwagger

launch_api = AppSwagger()
launch_api.register_apis()

async def main():
    config = uvicorn.Config(
        launch_api,
        host = 'localhost',
        port = 8000,
        workers = 5,
        log_level = 'debug',
        reload = False
        )
    server = uvicorn.Server(config)

    api = asyncio.create_task(server.serve())
    await asyncio.wait([api])

if __name__ == "__main__":
    asyncio.run(main())