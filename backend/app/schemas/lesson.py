from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LessonCreate(BaseModel):
    title: str
    content: Optional[str] = None


class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
