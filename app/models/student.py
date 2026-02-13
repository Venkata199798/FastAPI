# app/models/student.py
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Student(BaseModel):
    """
    English: Student table in database
    Telugu: డేటాబేస్ లో విద్యార్థి టేబుల్
    """
    __tablename__ = "students"
    
    # Basic Information / ప్రాథమిక సమాచారం
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15))
    
    # Academic Information / విద్యా సమాచారం
    student_id = Column(String(20), unique=True, nullable=False, index=True)
    grade = Column(Float)
    class_name = Column(String(20))
    
    # Status / స్థితి
    is_active = Column(Boolean, default=True)
    
    # Relationships / సంబంధాలు
    # courses = relationship("Course", secondary="student_courses", back_populates="students")