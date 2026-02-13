# app/crud/base.py
from typing import Generic, TypeVar, Type, Optional, List, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    English: Base class for CRUD operations
    Telugu: CRUD operations కోసం బేస్ క్లాస్
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        English: Initialize with SQLAlchemy model
        Telugu: SQLAlchemy మోడల్ తో ప్రారంభించండి
        """
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        English: Get a single record by ID
        Telugu: ID ద్వారా ఒక్క రికార్డ్ పొందండి
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        English: Get multiple records with pagination
        Telugu: పేజినేషన్ తో అనేక రికార్డ్స్ పొందండి
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        English: Create a new record
        Telugu: కొత్త రికార్డ్ సృష్టించండి
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        English: Update an existing record
        Telugu: ఉన్న రికార్డ్ అప్డేట్ చేయండి
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> ModelType:
        """
        English: Delete a record
        Telugu: రికార్డ్ తొలగించండి
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj