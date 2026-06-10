from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.student import Student
from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse,
)
from helpers import get_student_or_404

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post(
    "",
    response_model=StudentResponse,
    status_code=201
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Student)
        .filter(Student.email == student.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get(
    "",
    response_model=list[StudentResponse]
)
def get_students(
    grade_level: Optional[int] = None,
    is_enrolled: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    if grade_level is not None:
        query = query.filter(
            Student.grade_level == grade_level
        )

    if is_enrolled is not None:
        query = query.filter(
            Student.is_enrolled == is_enrolled
        )

    return query.all()

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return get_student_or_404(student_id, db)

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = get_student_or_404(student_id, db)

    duplicate = (
        db.query(Student)
        .filter(
            Student.email == student_data.email,
            Student.id != student_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    for key, value in student_data.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

@router.patch(
    "/{student_id}",
    response_model=StudentResponse
)
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(get_db)
):
    student = get_student_or_404(student_id, db)

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        duplicate = (
            db.query(Student)
            .filter(
                Student.email == update_data["email"],
                Student.id != student_id
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

@router.delete(
    "/{student_id}",
    status_code=204
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = get_student_or_404(student_id, db)

    db.delete(student)
    db.commit()

    return Response(status_code=204)

