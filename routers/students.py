from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.student import Student
from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse
)

from exceptions import (
    NotFoundException,
    DuplicateException,
    BadRequestException
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise NotFoundException(
            f"Student with id {student_id} not found"
        )

    return student

@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        Student.email == student_data.email
    ).first()

    if existing_student:
        raise DuplicateException(
            "A student with that email already exists"
        )

    student = Student(**student_data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise NotFoundException(
            f"Student with id {student_id} not found"
        )

    for key, value in student_data.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise NotFoundException(
            f"Student with id {student_id} not found"
        )

    updates = student_data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise NotFoundException(
            f"Student with id {student_id} not found"
        )

    if student.is_enrolled:
        raise BadRequestException(
            "Cannot delete a student who is currently enrolled"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }

