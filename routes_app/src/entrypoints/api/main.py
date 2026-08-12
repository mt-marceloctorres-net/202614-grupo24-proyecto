from fastapi import FastAPI

from config import Settings
from entrypoints.api.routers.route_router import router as route_router

app = FastAPI(title=Settings.app_name())
app.include_router(route_router)
