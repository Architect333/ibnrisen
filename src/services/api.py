from fastapi import FastAPI
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse


geograph_router = APIRouter()

@geograph_router.get("/", tags = ['GeoGraph'], status_code = status.HTTP_200_OK)
async def geograph():
    return FileResponse('www/index.html')


class AppSwagger(FastAPI):
    def __init__(self):
        # SWAGGER CONFIGURATION
        super().__init__(
            title = 'IBNRisen API',
            description = 'Intent-Based Networking Risen API Service',
            version = '0.0.1',
            docs_url = '/docs',
            redoc_url = '/redoc'
            )
    
    def register_apis(self):
        self.include_router(geograph_router, prefix = '/geograph')
