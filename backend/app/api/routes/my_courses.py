from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case

from app.db.deps import get_db
from app.core.auth import get_current_user
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress

router = APIRouter(prefix="/my", tags=["my"])


@router.get("/courses")
def my_courses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Student  -> enrolled courses with progress
    Instructor/Admin -> all courses with lesson count (we'll filter by owner in Step 2)
    """

    # -----------------------------
    # Instructor/Admin view (temp: show all)
    # -----------------------------
    if user.role in ("admin", "instructor"):
        lesson_counts = (
            select(Lesson.course_id, func.count(Lesson.id).label("total_lessons"))
            .group_by(Lesson.course_id)
            .subquery()
        )

        rows = db.execute(
            select(
                Course.id,
                Course.title,
                Course.description,
                Course.status,
                func.coalesce(lesson_counts.c.total_lessons, 0).label("total_lessons"),
            )
            .outerjoin(lesson_counts, lesson_counts.c.course_id == Course.id)
            .order_by(Course.id.desc())
        ).all()

        return [
            {
                "course_id": r.id,
                "title": r.title,
                "description": r.description,
                "status": r.status,
                "total_lessons": r.total_lessons,
                "completed_lessons": None,
                "percent": None,
            }
            for r in rows
        ]

    # -----------------------------
    # Student view (enrolled only)
    # -----------------------------
    enrolled = (
        select(Enrollment.course_id)
        .where(Enrollment.user_id == user.id)
        .subquery()
    )

    # total lessons per course
    totals = (
        select(Lesson.course_id, func.count(Lesson.id).label("total_lessons"))
        .where(Lesson.course_id.in_(select(enrolled.c.course_id)))
        .group_by(Lesson.course_id)
        .subquery()
    )

    # completed lessons per course (join lesson_progress -> lesson)
    completed = (
        select(
            Lesson.course_id.label("course_id"),
            func.count(func.distinct(LessonProgress.lesson_id)).label("completed_lessons"),
        )
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(LessonProgress.user_id == user.id)
        .where(LessonProgress.completed_at.is_not(None))
        .where(Lesson.course_id.in_(select(enrolled.c.course_id)))
        .group_by(Lesson.course_id)
        .subquery()
    )

    rows = db.execute(
        select(
            Course.id,
            Course.title,
            Course.description,
            Course.status,
            func.coalesce(totals.c.total_lessons, 0).label("total_lessons"),
            func.coalesce(completed.c.completed_lessons, 0).label("completed_lessons"),
        )
        .where(Course.id.in_(select(enrolled.c.course_id)))
        .outerjoin(totals, totals.c.course_id == Course.id)
        .outerjoin(completed, completed.c.course_id == Course.id)
        .order_by(Course.id.desc())
    ).all()

    result = []
    for r in rows:
        total = int(r.total_lessons or 0)
        done = int(r.completed_lessons or 0)
        percent = int((done / total) * 100) if total > 0 else 0

        result.append(
            {
                "course_id": r.id,
                "title": r.title,
                "description": r.description,
                "status": r.status,
                "total_lessons": total,
                "completed_lessons": done,
                "percent": percent,
            }
        )

    return result
