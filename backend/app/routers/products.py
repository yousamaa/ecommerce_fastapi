from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.Product)
def create(prod: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.products.create_product(db, prod)

@router.get("/", response_model=list[schemas.Product])
def list_all(skip: int=0, limit: int=100, db: Session = Depends(database.get_db)):
    return crud.products.list_products(db, skip, limit)

@router.get("/{prod_id}", response_model=schemas.Product)
def get_one(prod_id: int, db: Session = Depends(database.get_db)):
    p = crud.products.get_product(db, prod_id)
    if not p:
        raise HTTPException(404, "Product not found")
    return p
