from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, database

router = APIRouter(prefix="/sale-items", tags=["SaleItems"])

@router.get("/", response_model=list[schemas.SaleItem])
def list_all(
    product_id: Optional[int] = None,
    sale_id:    Optional[int] = None,
    skip:       int = 0,
    limit:      int = 100,
    db:         Session = Depends(database.get_db)
):
    return crud.sales_items.list_sale_items(db, product_id, sale_id, skip, limit)
