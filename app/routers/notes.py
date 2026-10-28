from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


def get_note_or_404(note_id: int, db: Session = Depends(get_db)) -> models.Note:
    note = crud.get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=List[schemas.NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)


@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note: models.Note = Depends(get_note_or_404)):
    return note


@router.post("", response_model=schemas.NoteOut, status_code=201)
def create_note(data: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, data)


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    data: schemas.NoteUpdate,
    note: models.Note = Depends(get_note_or_404),
    db: Session = Depends(get_db),
):
    return crud.update_note(db, note, data)


@router.delete("/{note_id}", status_code=204)
def delete_note(note: models.Note = Depends(get_note_or_404), db: Session = Depends(get_db)):
    crud.delete_note(db, note)
