import os

from fastapi import FastAPI

from . import models  # noqa: F401  (models registers the Note table)
from .database import Base, engine
from .errors import register_exception_handlers
from .routers import notes

app = FastAPI(title="team-notes-api")
register_exception_handlers(app)
app.include_router(notes.router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": os.getenv("APP_ENV", "development")}
