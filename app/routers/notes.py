from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .. import models, schemas
from ..repository import NoteRepository, get_repository

router = APIRouter(prefix="/notes", tags=["notes"])


def get_note_or_404(
    note_id: int, repo: NoteRepository = Depends(get_repository)
) -> models.Note:
    note = repo.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=List[schemas.NoteOut])
def list_notes(repo: NoteRepository = Depends(get_repository)):
    return repo.list()


@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note: models.Note = Depends(get_note_or_404)):
    return note


@router.post("", response_model=schemas.NoteOut, status_code=201)
def create_note(data: schemas.NoteCreate, repo: NoteRepository = Depends(get_repository)):
    return repo.create(data)


@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    data: schemas.NoteUpdate,
    note: models.Note = Depends(get_note_or_404),
    repo: NoteRepository = Depends(get_repository),
):
    return repo.update(note, data)


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note: models.Note = Depends(get_note_or_404),
    repo: NoteRepository = Depends(get_repository),
):
    repo.delete(note)
