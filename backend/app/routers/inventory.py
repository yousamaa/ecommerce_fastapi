from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=list[schemas.Inventory])
def list_all(skip: int=0, limit: int=100, db: Session = Depends(database.get_db)):
    return crud.inventory.list_inventory(db, skip, limit)

@router.get("/{prod_id}", response_model=schemas.Inventory)
def get_one(prod_id: int, db: Session = Depends(database.get_db)):
    inv = crud.inventory.get_inventory(db, prod_id)
    if not inv:
        raise HTTPException(404, "Inventory not found")
    return inv

@router.patch("/{prod_id}", response_model=schemas.Inventory)
def update_one(
    prod_id: int,
    upd:     schemas.InventoryCreate,
    db:      Session = Depends(database.get_db)
):
    return crud.inventory.update_inventory(
        db, prod_id, upd.quantity_on_hand, upd.reorder_threshold
    )

@router.get("/{prod_id}/history", response_model=list[schemas.InventoryHistory])
def history(prod_id: int, db: Session = Depends(database.get_db)):
    return crud.inventory_history.list_inventory_history(db, prod_id)
    
@router.post("/{prod_id}/history", response_model=schemas.InventoryHistory)
def record(
    prod_id:        int,
    record_in:      schemas.InventoryHistoryCreate,
    db:             Session = Depends(database.get_db)
):
    # override product_id from path
    record = record_in.copy(update={"product_id": prod_id})
    return crud.inventory_history.record_inventory_change(db, record)
