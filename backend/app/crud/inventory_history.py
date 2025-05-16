from sqlalchemy.orm import Session
from .. import models, schemas
from typing import Optional

def record_inventory_change(
    db:     Session,
    record: schemas.InventoryHistoryCreate
):
    ih = models.InventoryHistory(**record.dict())
    db.add(ih)
    db.commit()
    db.refresh(ih)
    return ih

def list_inventory_history(
    db:        Session,
    product_id: Optional[int] = None,
    skip:      int = 0,
    limit:     int = 100
):
    q = db.query(models.InventoryHistory)
    if product_id:
        q = q.filter(models.InventoryHistory.product_id == product_id)
    return q.offset(skip).limit(limit).all()
