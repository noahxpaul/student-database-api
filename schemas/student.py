from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    email: str
    grade_level: int
    gpa: Optional[float] = None
    is_enrolled: bool = True


class StudentUpdate(BaseModel):
    name: str
    email: str
    grade_level: int
    gpa: Optional[float] = None
    is_enrolled: bool


class StudentPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    grade_level: Optional[int] = None
    gpa: Optional[float] = None
    is_enrolled: Optional[bool] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    grade_level: int
    gpa: Optional[float]
    is_enrolled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)