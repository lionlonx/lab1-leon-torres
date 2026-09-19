from sqlalchemy.orm import Session

from . import models, schemas


def get_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.id).all()


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, content=note.content, author=note.author)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, note: schemas.NoteUpdate):
    db_note = get_note(db, note_id)
    if db_note is None:
        return None
    db_note.title = note.title
    db_note.content = note.content
    db_note.author = note.author
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    db_note = get_note(db, note_id)
    if db_note is None:
        return False
    db.delete(db_note)
    db.commit()
    return True
