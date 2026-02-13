# app/crud/student.py
from typing import Optional
from app.db.session import Session
from app.curd.base import CRUDBase
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    """
    English: Student-specific CRUD operations
    Telugu: విద్యార్థి-నిర్దిష్ట CRUD operations
    """
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[Student]:
        """
        English: Get student by email
        Telugu: ఇమెయిల్ ద్వారా విద్యార్థిని పొందండి
        """
        return db.query(Student).filter(Student.email == email).first()
    
    def get_by_student_id(self, db: Session, *, student_id: str) -> Optional[Student]:
        """
        English: Get student by student ID
        Telugu: విద్యార్థి ID ద్వారా విద్యార్థిని పొందండి
        """
        return db.query(Student).filter(Student.student_id == student_id).first()
    
    def search_by_name(self, db: Session, *, name: str) -> list[Student]:
        """
        English: Search students by name
        Telugu: పేరు ద్వారా విద్యార్థులను శోధించండి
        """
        search = f"%{name}%"
        return db.query(Student).filter(
            (Student.first_name.ilike(search)) | 
            (Student.last_name.ilike(search))
        ).all()

# Create instance / instance తయారు చేయండి
student = CRUDStudent(Student)