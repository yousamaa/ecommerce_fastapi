from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/", response_model=List[schemas.Inventory])
def list_inventory(
    skip:  int     = Query(0, ge=0),
    limit: int     = Query(100, ge=1),
    db:    Session = Depends(get_db),
):
    """
    List inventory with pagination.
    """
    return crud.inventory.list_inventory(db, skip, limit)


@router.get("/low-stock", response_model=List[schemas.Inventory])
def low_stock(
    db: Session = Depends(get_db),
):
    """
    Show only items at or below their reorder threshold.
    """
    all_inv = crud.inventory.list_inventory(db)
    return [
        inv for inv in all_inv
        if inv.quantity_on_hand <= inv.reorder_threshold
    ]


@router.get("/history", response_model=List[schemas.InventoryHistory])
def full_history(
    skip:       int           = Query(0, ge=0),
    limit:      int           = Query(100, ge=1),
    product_id: Optional[int] = Query(None),
    db:          Session      = Depends(get_db),
):
    """
    List all inventory-history entries, optionally filtered by product_id.
    """
    return crud.inventory_history.list_inventory_history(
        db, product_id=product_id, skip=skip, limit=limit
    )


@router.get("/{product_id}", response_model=schemas.Inventory)
def get_inventory_item(
    product_id: int,
    db:          Session = Depends(get_db),
):
    """
    Fetch the inventory row for a given product_id.
    """
    inv = crud.inventory.get_inventory(db, product_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inv


@router.patch("/{product_id}", response_model=schemas.Inventory)
def update_inventory_item(
    product_id: int,
    upd:        schemas.InventoryUpdate,
    db:          Session = Depends(get_db),
):
    """
    Update stock levels (and automatically log the change).
    """
    new_qty = upd.quantity_on_hand or 0
    new_rt  = upd.reorder_threshold or 0

    inv = crud.inventory.update_inventory(db, product_id, new_qty, new_rt)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # Log the adjustment
    change = new_qty - inv.quantity_on_hand
    if change:
        crud.inventory_history.record_inventory_change(
            db,
            inventory_id=inv.id,
            product_id=product_id,
            change_qty=change,
            reason="Manual adjustment"
        )
    return inv


@router.post("/{product_id}/history", response_model=schemas.InventoryHistory)
def record_inventory_change(
    product_id: int,
    rec_in:     schemas.InventoryHistoryCreate,
    db:          Session = Depends(get_db),
):
    """
    Record a new inventory-history entry for this product.
    """
    rec = rec_in.copy(update={"product_id": product_id})
    return crud.inventory_history.record_inventory_change(db, rec)
