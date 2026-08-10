from fastapi import FastAPI

from adapters.postgres.database import engine
from adapters.postgres.models import Base
from config import Settings
from entrypoints.api.routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=Settings.app_name)
app.include_router(user_router)
