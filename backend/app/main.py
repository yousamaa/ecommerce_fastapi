from fastapi import FastAPI

# import the router objects from each module
from app.routers.categories   import router as categories_router
from app.routers.products     import router as products_router
from app.routers.sales        import router as sales_router
from app.routers.sale_items   import router as sale_items_router
from app.routers.inventory    import router as inventory_router

app = FastAPI(title="E-commerce Admin API")

# wire up each router
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(sales_router)
app.include_router(sale_items_router)
app.include_router(inventory_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Admin API"}
