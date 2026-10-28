from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

# Los límites coinciden con las columnas de models.Note (String(200), String(120)).
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Author = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Content = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=5000)]


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime


class NoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title = Field(...)
    content: Content = Field(...)
    author: Author = Field(...)


class NoteUpdate(NoteCreate):
    """PUT reemplaza la nota completa: exige los mismos campos que al crearla."""
