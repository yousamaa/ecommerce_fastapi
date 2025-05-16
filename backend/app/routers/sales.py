from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/sales", tags=["sales"])


# 1. Create a new sale (with items)
@router.post("/", response_model=schemas.Sale)
def create_sale(
    sale_in: schemas.SaleCreate,
    db: Session = Depends(get_db),
):
    return crud.sales.create_sale(db, sale_in)


# 2. Revenue summary over a period
@router.get("/stats", response_model=List[schemas.RevenueResponse])
def read_revenue_stats(
    period:     str            = Query(..., regex="^(daily|weekly|monthly|yearly)$"),
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db:         Session        = Depends(get_db),
):
    try:
        return crud.sales.get_revenue_summary(db, period, start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3. Compare two date-ranges
@router.get("/compare", response_model=schemas.SalesComparison)
def compare_sales(
    p1_start:    date           = Query(..., alias="p1_start"),
    p1_end:      date           = Query(..., alias="p1_end"),
    p2_start:    date           = Query(..., alias="p2_start"),
    p2_end:      date           = Query(..., alias="p2_end"),
    category_id: Optional[int]  = Query(None),
    db:           Session       = Depends(get_db),
):
    return crud.sales.compare_periods(
        db, p1_start, p1_end, p2_start, p2_end, category_id
    )


# 4. Sales by product
@router.get(
    "/by-product/{product_id}",
    response_model=List[schemas.Sale],
    summary="List all sales containing a given product",
)
def sales_by_product(
    product_id:  int,
    start_date:  Optional[date] = Query(None),
    end_date:    Optional[date] = Query(None),
    skip:        int            = Query(0, ge=0),
    limit:       int            = Query(100, ge=1),
    db:           Session       = Depends(get_db),
):
    return crud.sales.get_sales(
        db,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category_id=None,
        skip=skip,
        limit=limit,
    )


# 5. Sales by category
@router.get(
    "/by-category/{category_id}",
    response_model=List[schemas.Sale],
    summary="List all sales for a given category",
)
def sales_by_category(
    category_id: int,
    start_date:  Optional[date] = Query(None),
    end_date:    Optional[date] = Query(None),
    skip:        int            = Query(0, ge=0),
    limit:       int            = Query(100, ge=1),
    db:           Session       = Depends(get_db),
):
    return crud.sales.get_sales(
        db,
        start_date=start_date,
        end_date=end_date,
        product_id=None,
        category_id=category_id,
        skip=skip,
        limit=limit,
    )


# 6. List & filter raw sales
@router.get("/", response_model=List[schemas.Sale])
def list_sales(
    start_date:  Optional[date] = Query(None),
    end_date:    Optional[date] = Query(None),
    product_id:  Optional[int]  = Query(None),
    category_id: Optional[int]  = Query(None),
    skip:        int            = Query(0, ge=0),
    limit:       int            = Query(100, ge=1),
    db:           Session       = Depends(get_db),
):
    return crud.sales.get_sales(
        db,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category_id=category_id,
        skip=skip,
        limit=limit,
    )


# 7. Fetch one sale by ID (must come last)
@router.get("/{sale_id}", response_model=schemas.Sale)
def get_one_sale(
    sale_id: int,
    db:      Session = Depends(get_db),
):
    s = crud.sales.get_sale(db, sale_id)
    if not s:
        raise HTTPException(status_code=404, detail="Sale not found")
    return s
