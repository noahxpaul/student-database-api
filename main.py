from fastapi import FastAPI

from database import Base, engine
from routers.students import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student CRUD API"
)

app.include_router(student_router)