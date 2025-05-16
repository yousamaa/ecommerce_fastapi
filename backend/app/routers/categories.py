from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.Category)
def create(cat: schemas.CategoryCreate, db: Session = Depends(database.get_db)):
    return crud.categories.create_category(db, cat)

@router.get("/", response_model=list[schemas.Category])
def list_all(skip: int=0, limit: int=100, db: Session = Depends(database.get_db)):
    return crud.categories.list_categories(db, skip, limit)

@router.get("/{cat_id}", response_model=schemas.Category)
def get_one(cat_id: int, db: Session = Depends(database.get_db)):
    c = crud.categories.get_category(db, cat_id)
    if not c:
        raise HTTPException(404, "Category not found")
    return c
