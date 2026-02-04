from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonOut

router = APIRouter(prefix="/courses", tags=["lessons"])


@router.get("/{course_id}/lessons", response_model=list[LessonOut])
def list_lessons(course_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    # ensure course exists
    if not db.get(Course, course_id):
        raise HTTPException(status_code=404, detail="Course not found")

    lessons = db.execute(
        select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.id.asc())
    ).scalars().all()
    return lessons


@router.post("/{course_id}/lessons", response_model=LessonOut, status_code=201)
def create_lesson(
    course_id: int,
    payload: LessonCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    if not db.get(Course, course_id):
        raise HTTPException(status_code=404, detail="Course not found")

    lesson = Lesson(course_id=course_id, title=payload.title, content=payload.content)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/lessons/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
