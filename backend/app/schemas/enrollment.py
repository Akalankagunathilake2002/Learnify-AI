from pydantic import BaseModel
from datetime import datetime


class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True
