from fastapi import FastAPI
from .routers import (
    categories,
    products,
    sales,
    sale_items,
    inventory,
)

app = FastAPI(title="E-commerce Admin API")

# include each router directly, not via .router
app.include_router(categories)
app.include_router(products)
app.include_router(sales)
app.include_router(sale_items)
app.include_router(inventory)


@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Admin API"}
