# app/api/v1/endpoints/students.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.curd.student import student as crud_student
from app.schemas.student import (StudentCreate,StudentUpdate,StudentResponse,StudentListResponse)
from app.core.config import settings

router = APIRouter()

# ==========================================
# CREATE STUDENT / విద్యార్థిని సృష్టించండి
# ==========================================

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(*,db: Session = Depends(get_db),student_in: StudentCreate):
    """
    English: Create a new student
    
    - **first_name**: Student's first name
    - **last_name**: Student's last name
    - **email**: Valid email address
    - **student_id**: Unique student ID
    - **grade**: Grade between 0-100
    
    Telugu: కొత్త విద్యార్థిని సృష్టించండి
    
    - **first_name**: విద్యార్థి మొదటి పేరు
    - **last_name**: విద్యార్థి చివరి పేరు
    - **email**: చెల్లుబాటు అయ్యే ఇమెయిల్ చిరునామా
    - **student_id**: ప్రత్యేకమైన విద్యార్థి ID
    - **grade**: 0-100 మధ్య గ్రేడ్
    """
    # Check if email exists / ఇమెయిల్ ఉందా అని చెక్ చేయండి
    student = crud_student.student.get_by_email(db, email=student_in.email)
    if student:
        raise HTTPException(
            status_code=400,
            detail="Email already registered / ఇమెయిల్ ఇప్పటికే రిజిస్టర్ చేయబడింది"
        )
    
    # Check if student_id exists / student_id ఉందా అని చెక్ చేయండి
    student = crud_student.student.get_by_student_id(db, student_id=student_in.student_id)
    if student:
        raise HTTPException(
            status_code=400,
            detail="Student ID already exists / విద్యార్థి ID ఇప్పటికే ఉంది"
        )
    
    # Create student / విద్యార్థిని సృష్టించండి
    student = crud_student.student.create(db, obj_in=student_in)
    return student


# ==========================================
# GET ALL STUDENTS / అన్ని విద్యార్థులను పొందండి
# ==========================================

@router.get("/", response_model=StudentListResponse)
def get_students(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE, 
        ge=1, 
        le=settings.MAX_PAGE_SIZE,
        description="Number of records to return"
    )
):
    """
    English: Get list of all students with pagination
    Telugu: పేజినేషన్ తో అన్ని విద్యార్థుల జాబితా పొందండి
    """
    students = crud_student.student.get_multi(db, skip=skip, limit=limit)
    total = db.query(crud_student.student.model).count()
    
    return {
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "students": students
    }


# ==========================================
# GET SINGLE STUDENT / ఒక్క విద్యార్థిని పొందండి
# ==========================================

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    English: Get a specific student by ID
    Telugu: ID ద్వారా నిర్దిష్ట విద్యార్థిని పొందండి
    """
    student = crud_student.student.get(db, id=student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found / విద్యార్థి కనుగొనబడలేదు"
        )
    return student


# ==========================================
# UPDATE STUDENT / విద్యార్థిని అప్డేట్ చేయండి
# ==========================================

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    English: Update student information
    Telugu: విద్యార్థి సమాచారాన్ని అప్డేట్ చేయండి
    """
    student = crud_student.student.get(db, id=student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found / విద్యార్థి కనుగొనబడలేదు"
        )
    
    student = crud_student.student.update(db, db_obj=student, obj_in=student_in)
    return student


# ==========================================
# DELETE STUDENT / విద్యార్థిని తొలగించండి
# ==========================================

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    English: Delete a student
    Telugu: విద్యార్థిని తొలగించండి
    """
    student = crud_student.student.get(db, id=student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found / విద్యార్థి కనుగొనబడలేదు"
        )
    
    crud_student.student.delete(db, id=student_id)
    return {"message": "Student deleted successfully / విద్యార్థి విజయవంతంగా తొలగించబడింది"}


# ==========================================
# SEARCH STUDENTS / విద్యార్థులను శోధించండి
# ==========================================

@router.get("/search/", response_model=List[StudentResponse])
def search_students(
    name: str = Query(..., min_length=2, description="Search by name"),
    db: Session = Depends(get_db)
):
    """
    English: Search students by name
    Telugu: పేరు ద్వారా విద్యార్థులను శోధించండి
    """
    students = crud_student.student.search_by_name(db, name=name)
    return students