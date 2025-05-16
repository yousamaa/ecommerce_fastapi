from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from .. import schemas, crud, database

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=schemas.Sale)
def create(sale: schemas.SaleCreate, db: Session = Depends(database.get_db)):
    return crud.sales.create_sale(db, sale)

@router.get("/", response_model=list[schemas.Sale])
def list_all(
    start_date: Optional[datetime] = Query(None),
    end_date:   Optional[datetime] = Query(None),
    skip:       int = 0,
    limit:      int = 100,
    db:         Session = Depends(database.get_db)
):
    return crud.sales.list_sales(db, start_date, end_date, skip, limit)

@router.get("/{sale_id}", response_model=schemas.Sale)
def get_one(sale_id: int, db: Session = Depends(database.get_db)):
    s = crud.sales.get_sale(db, sale_id)
    if not s:
        raise HTTPException(404, "Sale not found")
    return s
