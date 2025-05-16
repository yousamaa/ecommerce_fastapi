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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

# --- Inventory History ---
class InventoryHistoryBase(BaseModel):
    product_id: int
    change_qty: int
    reason: str

class InventoryHistoryCreate(InventoryHistoryBase):
    pass

class InventoryHistory(InventoryHistoryBase):
    id: int
    changed_at: datetime

class Config:
    model_config = ConfigDict(from_attributes=True)
