from sqlalchemy.orm import Session
from .. import models, schemas
import datetime
from sqlalchemy import func
from datetime import date
from typing import List, Optional

def create_sale(db: Session, sale_in: schemas.SaleCreate):
    db_sale = models.Sale(
        sale_date=sale_in.sale_date,
        customer_name=sale_in.customer_name,
        total_amount=sale_in.total_amount
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    for item in sale_in.items:
        db_item = models.SaleItem(
            sale_id=db_sale.id,
            **item.dict()
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def list_sales(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date:   Optional[datetime] = None,
    skip:       int = 0,
    limit:      int = 100
):
    q = db.query(models.Sale)
    if start_date:
        q = q.filter(models.Sale.sale_date >= start_date)
    if end_date:
        q = q.filter(models.Sale.sale_date <= end_date)
    return q.offset(skip).limit(limit).all()


def get_sales(
    db: Session,
    start_date: Optional[date] = None,
    end_date:   Optional[date] = None,
    product_id: Optional[int] = None,
    category_id:Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Sale]:
    q = db.query(models.Sale)
    if start_date:
        q = q.filter(models.Sale.sale_date >= start_date)
    if end_date:
        q = q.filter(models.Sale.sale_date <= end_date)
    if product_id or category_id:
        q = q.join(models.SaleItem, models.Sale.id == models.SaleItem.sale_id) \
             .join(models.Product, models.SaleItem.product_id == models.Product.id)
        if product_id:
            q = q.filter(models.SaleItem.product_id == product_id)
        if category_id:
            q = q.filter(models.Product.category_id == category_id)
    return q.offset(skip).limit(limit).all()

def get_revenue_summary(
    db: Session,
    period: str,  # "daily"|"weekly"|"monthly"|"yearly"
    start_date: Optional[date] = None,
    end_date:   Optional[date] = None,
) -> List[schemas.RevenueResponse]:
    sale = models.Sale
    # pick grouping function
    if period == "daily":
        grp = func.date(sale.sale_date)
    elif period == "weekly":
        grp = func.week(sale.sale_date)
    elif period == "monthly":
        grp = func.month(sale.sale_date)
    elif period == "yearly":
        grp = func.year(sale.sale_date)
    else:
        raise ValueError("Invalid period")

    q = db.query(
        grp.label("period"),
        func.sum(sale.total_amount).label("total_amount")
    )
    if start_date:
        q = q.filter(sale.sale_date >= start_date)
    if end_date:
        q = q.filter(sale.sale_date <= end_date)
    q = q.group_by(grp).order_by(grp)

    return [
        schemas.RevenueResponse(period=str(r.period), total_amount=float(r.total_amount))
        for r in q.all()
    ]

def compare_periods(
    db: Session,
    p1_start:   date,
    p1_end:     date,
    p2_start:   date,
    p2_end:     date,
    category_id: Optional[int] = None,
) -> schemas.SalesComparison:
    # helper to sum revenue in a range
    def sum_range(start: date, end: date) -> float:
        q = db.query(func.sum(models.Sale.total_amount))
        q = q.filter(models.Sale.sale_date >= start,
                     models.Sale.sale_date <= end)
        if category_id:
            q = q.join(models.SaleItem)\
                 .join(models.Product)\
                 .filter(models.Product.category_id == category_id)
        total = q.scalar() or 0.0
        return float(total)

    rev1 = sum_range(p1_start, p1_end)
    rev2 = sum_range(p2_start, p2_end)
    diff = rev2 - rev1
    pct  = (diff / rev1 * 100) if rev1 != 0 else None

    return schemas.SalesComparison(
        period1=schemas.PeriodRevenue(
            start=p1_start.isoformat(),
            end  =p1_end.isoformat(),
            revenue=rev1
        ),
        period2=schemas.PeriodRevenue(
            start=p2_start.isoformat(),
            end  =p2_end.isoformat(),
            revenue=rev2
        ),
        difference     = diff,
        percent_change = pct
    )