from sqlalchemy.orm import Session
from typing import Optional
from .. import models

def list_sale_items(
    db: Session,
    product_id: Optional[int] = None,
    sale_id:    Optional[int] = None,
    skip:       int = 0,
    limit:      int = 100
):
    q = db.query(models.SaleItem)
    if product_id:
        q = q.filter(models.SaleItem.product_id == product_id)
    if sale_id:
        q = q.filter(models.SaleItem.sale_id == sale_id)
    return q.offset(skip).limit(limit).all()
