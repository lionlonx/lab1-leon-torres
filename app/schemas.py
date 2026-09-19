from datetime import datetime

from pydantic import BaseModel, ConfigDict

from typing import Optional


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime

class NoteBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = "Anonymous"

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
