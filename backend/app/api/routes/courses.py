from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.deps import get_db
from app.core.auth import get_current_user
from app.core.rbac import require_role
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut
from app.core.rbac import require_role

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = select(Course).order_by(Course.id.desc())

    # ✅ students only see published
    if user.role == "student":
        q = q.where(Course.status == "published")

    return db.execute(q).scalars().all()



@router.post("", response_model=CourseOut, status_code=201)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("instructor", "admin")),  # ✅ only instructor/admin
):
    course = Course(title=payload.title, description=payload.description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    # students can view
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course




@router.post("/{course_id}/publish", status_code=200)
def publish_course(
    course_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("instructor", "admin")),
):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.status = "published"
    db.commit()
    return {"message": "published"}


@router.post("/{course_id}/unpublish", status_code=200)
def unpublish_course(
    course_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("instructor", "admin")),
):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.status = "draft"
    db.commit()
    return {"message": "draft"}
