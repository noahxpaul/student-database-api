from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    grade_level = Column(Integer, nullable=False)
    gpa = Column(Float, nullable=True)
    is_enrolled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)