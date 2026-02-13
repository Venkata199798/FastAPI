# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import students

api_router = APIRouter()

# Include all endpoint routers / అన్ని endpoint routers ను చేర్చండి
api_router.include_router(
    students.router, 
    prefix="/students", 
    tags=["students"]
)

# Add more routers here / ఇక్కడ మరిన్ని routers జోడించండి
# api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
# api_router.include_router(courses.router, prefix="/courses", tags=["courses"])