from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None  # ✅ NEW

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    video_url: Optional[str] = None  # ✅ NEW
    created_at: datetime

    class Config:
        from_attributes = True
