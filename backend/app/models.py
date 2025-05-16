from sqlalchemy import (
    Column, Integer, String, DECIMAL, DateTime,
    ForeignKey, func, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    parent   = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("sku", name="uq_products_sku"),
        Index("ix_products_category", "category_id"),
    )
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    sku         = Column(String(100), nullable=False)
    price       = Column(DECIMAL(10,2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    category           = relationship("Category", back_populates="products")
    sale_items         = relationship("SaleItem",    back_populates="product")
    inventory          = relationship("Inventory",   back_populates="product", uselist=False)
    inventory_history  = relationship("InventoryHistory", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = (
        Index("ix_sales_date", "sale_date"),
    )
    id            = Column(Integer, primary_key=True, index=True)
    sale_date     = Column(DateTime(timezone=True), nullable=False)
    customer_name = Column(String(200), nullable=True)
    total_amount  = Column(DECIMAL(12,2), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = "sale_items"
    __table_args__ = (
        Index("ix_sale_items_product", "product_id"),
    )
    id         = Column(Integer, primary_key=True, index=True)
    sale_id    = Column(Integer, ForeignKey("sales.id"),    nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"),  nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    line_total = Column(DECIMAL(12,2), nullable=False)

    sale    = relationship("Sale",    back_populates="items")
    product = relationship("Product", back_populates="sale_items")

# class Inventory(Base):
#     __tablename__ = "inventory"
#     id                 = Column(Integer, primary_key=True, index=True)
#     product_id         = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
#     quantity_on_hand   = Column(Integer, nullable=False)
#     reorder_threshold  = Column(Integer, nullable=False)



#     product = relationship("Product", back_populates="inventory")
#     logs    = relationship("InventoryHistory", back_populates="inventory")

# class InventoryHistory(Base):
#     __tablename__ = "inventory_history"
#     id         = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     change_qty = Column(Integer, nullable=False)
#     reason     = Column(String(255), nullable=False)
#     changed_at = Column(DateTime(timezone=True), server_default=func.now())

#     product   = relationship("Product", back_populates="inventory_history")
#     inventory = relationship(
#         "Inventory",
#         primaryjoin="InventoryHistory.product_id==Inventory.product_id",
#         back_populates="logs")
class Inventory(Base):
    __tablename__ = "inventory"

    id                = Column(Integer, primary_key=True, index=True)
    product_id        = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    quantity_on_hand  = Column(Integer, nullable=False)
    reorder_threshold = Column(Integer, nullable=False)

    # relationships
    product = relationship("Product", back_populates="inventory")
    logs    = relationship(
        "InventoryHistory",
        back_populates="inventory",
        cascade="all, delete-orphan"
    )

class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id           = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id"),   nullable=False)
    change_qty   = Column(Integer, nullable=False)
    reason       = Column(String(255), nullable=False)
    changed_at   = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    inventory = relationship("Inventory", back_populates="logs")
    product   = relationship("Product",   back_populates="inventory_history")