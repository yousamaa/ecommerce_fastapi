from app.database import SessionLocal, Base
from sqlalchemy import text
from app import models
from datetime import datetime, timedelta


def clear_tables(db):
    # If you’re on MySQL, temporarily disable FK checks so deletes don’t error out
    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    # Delete from every table, child first
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.commit()

def populate_db():
    db = SessionLocal()

    clear_tables(db)

    # 1. Add parent Categories
    electronics   = models.Category(name="Electronics")
    clothing      = models.Category(name="Clothing")
    home_kitchen  = models.Category(name="Home & Kitchen")
    beauty        = models.Category(name="Beauty")
    toys          = models.Category(name="Toys")

    db.add_all([electronics, clothing, home_kitchen, beauty, toys])
    db.commit()  # so each .id is populated

    # 2. Add child Categories using parent objects
    laptops       = models.Category(name="Laptops",       parent_id=electronics.id)
    smartphones   = models.Category(name="Smartphones",   parent_id=electronics.id)
    t_shirts      = models.Category(name="T-Shirts",      parent_id=clothing.id)
    jeans         = models.Category(name="Jeans",         parent_id=clothing.id)
    vacuums       = models.Category(name="Vacuums",       parent_id=home_kitchen.id)
    coffee_makers = models.Category(name="Coffee Makers", parent_id=home_kitchen.id)

    db.add_all([laptops, smartphones, t_shirts, jeans, vacuums, coffee_makers])
    db.commit()

    # 3. Add Products
    products = [
        models.Product(name="Apple MacBook Pro 16-inch",    sku="MBP-16-2025",        price=2499.99, category_id=laptops.id),
        models.Product(name="Samsung Galaxy S21",           sku="SGS21-2025",         price=799.99,  category_id=smartphones.id),
        models.Product(name="Sony WH-1000XM4 Headphones",   sku="WH-1000XM4",         price=348.00,  category_id=electronics.id),
        models.Product(name="Nike Air Force 1 Sneakers",   sku="AF1-2025",           price=90.00,   category_id=t_shirts.id),
        models.Product(name="Levi's 501 Original Jeans",    sku="501-2025",           price=59.99,   category_id=jeans.id),
        models.Product(name="Dyson V11 Cordless Vacuum",    sku="DY-V11-2025",        price=599.99,  category_id=vacuums.id),
        models.Product(name="Keurig K-Elite Coffee Maker",  sku="K-Elite-2025",       price=129.99,  category_id=coffee_makers.id),
        models.Product(name="Olay Regenerist Face Cream",   sku="Olay-2025",          price=24.99,   category_id=beauty.id),
        models.Product(name="LEGO Star Wars Millennium Falcon", sku="LEGO-SW-2025",   price=159.99,  category_id=toys.id),
    ]
    db.add_all(products)
    db.commit()

    # 4. Add Sales & SaleItems
    now = datetime.now()
    sales = [
        models.Sale(total_amount=2500.00, sale_date=now - timedelta(days=10)),
        models.Sale(total_amount=850.00,  sale_date=now - timedelta(days=15)),
        models.Sale(total_amount=120.00,  sale_date=now - timedelta(days=20)),
        models.Sale(total_amount=600.00,  sale_date=now - timedelta(days=5)),
        models.Sale(total_amount=340.00,  sale_date=now - timedelta(days=1)),
    ]
    db.add_all(sales)
    db.commit()

    sale_items = [
        models.SaleItem(sale_id=sales[0].id, product_id=products[0].id, quantity=1, unit_price=2499.99, line_total=2499.99),
        models.SaleItem(sale_id=sales[1].id, product_id=products[1].id, quantity=1, unit_price=799.99,  line_total=799.99),
        models.SaleItem(sale_id=sales[2].id, product_id=products[7].id, quantity=1, unit_price=24.99,   line_total=24.99),
        models.SaleItem(sale_id=sales[3].id, product_id=products[4].id, quantity=2, unit_price=59.99,   line_total=119.98),
        models.SaleItem(sale_id=sales[4].id, product_id=products[2].id, quantity=1, unit_price=348.00,  line_total=348.00),
    ]
    db.add_all(sale_items)
    db.commit()

    # 5. Add Inventory entries
    inventory_data = [
        models.Inventory(product_id=products[0].id, quantity_on_hand=50,  reorder_threshold=5),
        models.Inventory(product_id=products[1].id, quantity_on_hand=200, reorder_threshold=20),
        models.Inventory(product_id=products[2].id, quantity_on_hand=150, reorder_threshold=15),
        models.Inventory(product_id=products[3].id, quantity_on_hand=30,  reorder_threshold=5),
        models.Inventory(product_id=products[4].id, quantity_on_hand=100, reorder_threshold=10),
        models.Inventory(product_id=products[5].id, quantity_on_hand=120, reorder_threshold=20),
        models.Inventory(product_id=products[6].id, quantity_on_hand=80,  reorder_threshold=8),
        models.Inventory(product_id=products[7].id, quantity_on_hand=300, reorder_threshold=30),
        models.Inventory(product_id=products[8].id, quantity_on_hand=50,  reorder_threshold=5),
    ]
    db.add_all(inventory_data)
    db.commit()

    # 6. Add InventoryHistory for each inventory
    history_entries = []
    for inv in inventory_data:
        # initial stock entry 30 days ago:
        history_entries.append(
            models.InventoryHistory(
                inventory_id=inv.id,
                product_id=inv.product_id,
                change_qty=inv.quantity_on_hand,
                reason="Initial stock",
                changed_at=now - timedelta(days=30),
            )
        )
        # sample sale 7 days ago:
        history_entries.append(
            models.InventoryHistory(
                inventory_id=inv.id,
                product_id=inv.product_id,
                change_qty=-2,
                reason="Sample sale",
                changed_at=now - timedelta(days=7),
            )
        )

    db.add_all(history_entries)
    db.commit()

    print("Database populated with demo data!")

if __name__ == "__main__":
    populate_db()
