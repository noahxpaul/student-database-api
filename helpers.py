from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.student import Student


def get_student_or_404(student_id: int, db: Session):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student