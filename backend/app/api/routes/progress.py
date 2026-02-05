from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress

router = APIRouter(tags=["progress"])


@router.post("/lessons/{lesson_id}/complete", status_code=201)
def complete_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing = db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id,
            LessonProgress.lesson_id == lesson_id
        )
    ).scalar_one_or_none()

    if existing:
        return {"status": "already_completed"}

    row = LessonProgress(user_id=user.id, lesson_id=lesson_id)
    db.add(row)
    db.commit()
    return {"status": "completed"}


@router.delete("/lessons/{lesson_id}/complete")
def uncomplete_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id,
            LessonProgress.lesson_id == lesson_id
        )
    ).scalar_one_or_none()

    if not existing:
        return {"status": "not_completed"}

    db.delete(existing)
    db.commit()
    return {"status": "uncompleted"}


@router.get("/courses/{course_id}/progress")
def course_progress(course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.execute(
        select(func.count(Lesson.id)).where(Lesson.course_id == course_id)
    ).scalar_one()

    completed = db.execute(
        select(func.count(LessonProgress.id))
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(Lesson.course_id == course_id, LessonProgress.user_id == user.id)
    ).scalar_one()

    return {
        "course_id": course_id,
        "total_lessons": total,
        "completed_lessons": completed,
        "percent": 0 if total == 0 else round((completed / total) * 100)
    }
