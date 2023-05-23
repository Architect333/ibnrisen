import asyncio
import uvicorn
from fastapi import FastAPI, status

geograph_api = FastAPI()

@geograph_api.get("/", status_code = status.HTTP_200_OK)
async def geograph():
    return {"message": "Hello World"}
    #return index.html

async def main():
    config = uvicorn.Config(
        'server:geograph_api',
        host = 'localhost',
        port = 8000,
        workers = 5,
        log_level = 'debug',
        reload = True
        )
    server = uvicorn.Server(config)

    api = asyncio.create_task(server.serve())
    await asyncio.wait([api])

if __name__ == "__main__":
    asyncio.run(main())