from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentOut

router = APIRouter(tags=["enrollments"])


@router.post("/courses/{course_id}/enroll", response_model=EnrollmentOut, status_code=201)
def enroll(course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.execute(
        select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id)
    ).scalar_one_or_none()

    if existing:
        return existing

    enr = Enrollment(user_id=user.id, course_id=course_id)
    db.add(enr)
    db.commit()
    db.refresh(enr)
    return enr


@router.get("/me/courses")
def my_courses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # returns courses joined by this user (simple list of course objects)
    rows = db.execute(
        select(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .where(Enrollment.user_id == user.id)
        .order_by(Course.id.desc())
    ).scalars().all()

    return rows
