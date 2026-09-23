from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from core.config import settings

from api.agent import router as agent_router
from api.auth import router as auth_router

from models.base import Base
from core.database import engine


@asynccontextmanager
async def lifespan(app : FastAPI) :
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(auth_router)