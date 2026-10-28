from typing import List, Optional, Protocol

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db


class NoteRepository(Protocol):
    """Lo que los endpoints necesitan para guardar notas, sin saber cÃ³mo se guardan."""

    def list(self) -> List[models.Note]: ...

    def get(self, note_id: int) -> Optional[models.Note]: ...

    def create(self, data: schemas.NoteCreate) -> models.Note: ...

    def update(self, note: models.Note, data: schemas.NoteUpdate) -> models.Note: ...

    def delete(self, note: models.Note) -> None: ...


class SqlAlchemyNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def _commit(self) -> None:
        # Si el commit falla, la sesión queda inutilizable hasta hacer rollback.
        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def list(self) -> List[models.Note]:
        return self.db.query(models.Note).order_by(models.Note.id).all()

    def get(self, note_id: int) -> Optional[models.Note]:
        return self.db.get(models.Note, note_id)

    def create(self, data: schemas.NoteCreate) -> models.Note:
        note = models.Note(**data.model_dump())
        self.db.add(note)
        self._commit()
        self.db.refresh(note)
        return note

    def update(self, note: models.Note, data: schemas.NoteUpdate) -> models.Note:
        for field, value in data.model_dump().items():
            setattr(note, field, value)
        self._commit()
        self.db.refresh(note)
        return note

    def delete(self, note: models.Note) -> None:
        self.db.delete(note)
        self._commit()


def get_repository(db: Session = Depends(get_db)) -> NoteRepository:
    return SqlAlchemyNoteRepository(db)
