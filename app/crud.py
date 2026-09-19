from sqlalchemy.orm import Session

from . import models


def get_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.id).all()


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()
