from sqlalchemy.orm import Session
from .. import models, schemas

def create_category(db: Session, cat: schemas.CategoryCreate):
    db_cat = models.Category(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_category(db: Session, cat_id: int):
    return db.query(models.Category).filter(models.Category.id == cat_id).first()

def list_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()
