from typing import List, Optional, Protocol

from fastapi import Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db


class NoteRepository(Protocol):
    """Lo que los endpoints necesitan para guardar notas, sin saber cómo se guardan."""

    def list(self) -> List[models.Note]: ...

    def get(self, note_id: int) -> Optional[models.Note]: ...

    def create(self, data: schemas.NoteCreate) -> models.Note: ...

    def update(self, note: models.Note, data: schemas.NoteUpdate) -> models.Note: ...

    def delete(self, note: models.Note) -> None: ...


class SqlAlchemyNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[models.Note]:
        return self.db.query(models.Note).order_by(models.Note.id).all()

    def get(self, note_id: int) -> Optional[models.Note]:
        return self.db.get(models.Note, note_id)

    def create(self, data: schemas.NoteCreate) -> models.Note:
        note = models.Note(**data.model_dump())
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: models.Note, data: schemas.NoteUpdate) -> models.Note:
        for field, value in data.model_dump().items():
            setattr(note, field, value)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: models.Note) -> None:
        self.db.delete(note)
        self.db.commit()


def get_repository(db: Session = Depends(get_db)) -> NoteRepository:
    return SqlAlchemyNoteRepository(db)
