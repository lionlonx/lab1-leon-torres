import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

INSECURE_PASSWORDS = {"", "change_this_password", "postgres", "password", "admin"}


def build_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    password = os.getenv("DB_PASSWORD", "")
    if password in INSECURE_PASSWORDS:
        raise RuntimeError(
            "DB_PASSWORD no está definido o usa un valor de ejemplo; configúralo en .env"
        )
    user = os.getenv("DB_USER", "team_notes_user")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "team_notes")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


DATABASE_URL = build_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from . import models  # noqa: F401  (registra la tabla notes en Base.metadata)

    Base.metadata.create_all(bind=engine)
