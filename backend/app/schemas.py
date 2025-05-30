from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from pydantic import ConfigDict


# --- Categories ---
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: List["Category"] = []

    class Config:
        model_config = ConfigDict(from_attributes=True)

Category.update_forward_refs()

# --- Products ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category

    class Config:
        model_config = ConfigDict(from_attributes=True)

# --- Sale Items (used inside Sale) ---
class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    line_total: float

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    id: int
    sale_id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

# --- Sales ---
class SaleBase(BaseModel):
    sale_date: datetime
    customer_name: Optional[str] = None
    total_amount: float

class SaleCreate(SaleBase):
    items: List[SaleItemCreate]

class Sale(SaleBase):
    id: int
    created_at: datetime
    items: List[SaleItem] = []

    class Config:
        model_config = ConfigDict(from_attributes=True)

# --- Inventory ---
class InventoryBase(BaseModel):
    product_id: int
    quantity_on_hand: int
    reorder_threshold: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

# --- Inventory History ---
class InventoryHistoryBase(BaseModel):
    product_id: int
    inventory_id: int
    change_qty: int
    reason: str

class InventoryHistoryCreate(InventoryHistoryBase):
    pass

class InventoryHistory(InventoryHistoryBase):
    id: int
    changed_at: datetime

class Config:
    model_config = ConfigDict(from_attributes=True)


# ——— Sales analytics response ———
class RevenueResponse(BaseModel):
    period: str
    total_amount: float

    class Config:
        model_config = ConfigDict(from_attributes=True)

# ——— Inventory updates ———
class InventoryUpdate(BaseModel):
    quantity_on_hand: Optional[int] = None
    reorder_threshold: Optional[int] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)

# -- for /sales/compare --
class PeriodRevenue(BaseModel):
    start:   str
    end:     str
    revenue: float

    class Config:
        model_config = ConfigDict(from_attributes=True)

class SalesComparison(BaseModel):
    period1:        PeriodRevenue
    period2:        PeriodRevenue
    difference:     float
    percent_change: Optional[float]

    class Config:
        model_config = ConfigDict(from_attributes=True)