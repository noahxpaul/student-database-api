# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import (
    NotFoundException,
    DuplicateException,
    BadRequestException
)

from routers.students import router as student_router

app = FastAPI()

# 404 Handler
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": exc.detail
        }
    )

# 409 Handler
@app.exception_handler(DuplicateException)
async def duplicate_exception_handler(
    request: Request,
    exc: DuplicateException
):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Duplicate Resource",
            "message": exc.detail
        }
    )

# 400 Handler
@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(
    request: Request,
    exc: BadRequestException
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "message": exc.detail
        }
    )

app.include_router(student_router)