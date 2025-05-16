from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
import datetime

def create_sale(db: Session, sale_in: schemas.SaleCreate):
    db_sale = models.Sale(
        sale_date=sale_in.sale_date,
        customer_name=sale_in.customer_name,
        total_amount=sale_in.total_amount
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    for item in sale_in.items:
        db_item = models.SaleItem(
            sale_id=db_sale.id,
            **item.dict()
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def list_sales(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date:   Optional[datetime] = None,
    skip:       int = 0,
    limit:      int = 100
):
    q = db.query(models.Sale)
    if start_date:
        q = q.filter(models.Sale.sale_date >= start_date)
    if end_date:
        q = q.filter(models.Sale.sale_date <= end_date)
    return q.offset(skip).limit(limit).all()
