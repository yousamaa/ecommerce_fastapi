from sqlalchemy.orm import Session
from .. import models, schemas

def create_product(db: Session, prod: schemas.ProductCreate):
    db_prod = models.Product(**prod.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def get_product(db: Session, prod_id: int):
    return db.query(models.Product).filter(models.Product.id == prod_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()
