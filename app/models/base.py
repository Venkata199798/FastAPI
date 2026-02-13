# app/models/base.py
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class BaseModel(Base):
    """
    English: Base model with common fields for all tables
    Telugu: అన్ని టేబుల్స్ కోసం సాధారణ ఫీల్డ్స్ తో బేస్ మోడల్
    """
    __abstract__ = True  # This won't create a table
                          
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())