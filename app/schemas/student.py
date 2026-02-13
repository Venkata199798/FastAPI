# app/schemas/student.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ==========================================
# Base Schema / బేస్ Schema
# ==========================================

class StudentBase(BaseModel):
    """
    English: Base schema with common fields
    Telugu: సాధారణ ఫీల్డ్స్ తో బేస్ schema
    """
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    class_name: Optional[str] = None


# ==========================================
# Create Schema / సృష్టించు Schema
# ==========================================

class StudentCreate(StudentBase):
    """
    English: Schema for creating a new student
    Telugu: కొత్త విద్యార్థిని సృష్టించడానికి schema
    """
    student_id: str = Field(min_length=5, max_length=20)
    grade: float = Field(ge=0, le=100)


# ==========================================
# Update Schema / అప్డేట్ Schema
# ==========================================

class StudentUpdate(BaseModel):
    """
    English: Schema for updating student (all fields optional)
    Telugu: విద్యార్థిని అప్డేట్ చేయడానికి schema (అన్ని ఫీల్డ్స్ ఐచ్ఛికం)
    """
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    grade: Optional[float] = Field(None, ge=0, le=100)
    class_name: Optional[str] = None
    is_active: Optional[bool] = None


# ==========================================
# Response Schema / రెస్పాన్స్ Schema
# ==========================================

class StudentResponse(StudentBase):
    """
    English: Schema for returning student data
    Telugu: విద్యార్థి డేటాను return చేయడానికి schema
    """
    id: int
    student_id: str
    grade: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==========================================
# List Response / జాబితా రెస్పాన్స్
# ==========================================

class StudentListResponse(BaseModel):
    """
    English: Schema for paginated student list
    Telugu: పేజినేట్ చేయబడిన విద్యార్థుల జాబితా కోసం schema
    """
    total: int
    page: int
    page_size: int
    students: list[StudentResponse]