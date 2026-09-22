from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings

@asynccontextmanager
async def lifespan(app : FastAPI) :
    yield

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan
)

