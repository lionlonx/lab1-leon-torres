from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime
