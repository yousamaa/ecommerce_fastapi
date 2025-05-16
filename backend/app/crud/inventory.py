from sqlalchemy.orm import Session
from .. import models, schemas

def get_inventory(db: Session, prod_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == prod_id).first()

def list_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

def update_inventory(
    db: Session,
    prod_id:           int,
    quantity_on_hand:  int,
    reorder_threshold: int
):
    inv = get_inventory(db, prod_id)
    if not inv:
        inv = models.Inventory(
            product_id=prod_id,
            quantity_on_hand=quantity_on_hand,
            reorder_threshold=reorder_threshold
        )
        db.add(inv)
    else:
        inv.quantity_on_hand  = quantity_on_hand
        inv.reorder_threshold = reorder_threshold
    db.commit()
    db.refresh(inv)
    return inv
