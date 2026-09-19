from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class NoteUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime
