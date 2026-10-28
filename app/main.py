import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .errors import register_exception_handlers
from .routers import notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="team-notes-api", lifespan=lifespan)
register_exception_handlers(app)
app.include_router(notes.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": os.getenv("APP_ENV", "development")}
