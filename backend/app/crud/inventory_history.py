from sqlalchemy.orm import Session
from .. import models, schemas
from typing import Optional, List

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

def record_inventory_change(
    db: Session,
    inventory_id: int,
    product_id:   int,
    change_qty:   int,
    reason:       str
):
    entry = models.InventoryHistory(
        inventory_id=inventory_id,
        product_id=product_id,
        change_qty=change_qty,
        reason=reason
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def list_inventory_history(
    db: Session,
    inventory_id: Optional[int] = None,
    product_id:   Optional[int] = None
) -> List[models.InventoryHistory]:
    q = db.query(models.InventoryHistory)
    if inventory_id:
        q = q.filter(models.InventoryHistory.inventory_id == inventory_id)
    if product_id:
        q = q.filter(models.InventoryHistory.product_id == product_id)
    return q.order_by(models.InventoryHistory.changed_at.desc()).all()