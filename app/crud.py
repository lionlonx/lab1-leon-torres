from sqlalchemy.orm import Session

from . import models, schemas


def get_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.id).all()


def get_note(db: Session, note_id: int):
    return db.get(models.Note, note_id)


def create_note(db: Session, data: schemas.NoteCreate) -> models.Note:
    note = models.Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note: models.Note, data: schemas.NoteUpdate) -> models.Note:
    for field, value in data.model_dump().items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: models.Note) -> None:
    db.delete(note)
    db.commit()
