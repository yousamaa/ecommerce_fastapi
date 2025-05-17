# E-commerce Admin API

A FastAPI-based backend for managing products, categories, inventory, and sales for an e-commerce platform. This project provides a RESTful API for administrative operations such as product management, inventory tracking, sales analytics, and more.

## Features

- Product and category management
- Inventory tracking and history
- Sales and sales item management
- Sales analytics and revenue comparison
- Built with FastAPI, SQLAlchemy, and Alembic

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ecommerce_fastapi/backend
```

### 2. Create and Configure Environment

- Copy `.env.example` to `.env` and set your database URL (MySQL recommended):
  ```env
  DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/<database>
  ```

### 3. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. (Optional) Seed Demo Data

```bash
python seed_data.py
```

### 6. Start the API Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000/`.

## Dependencies

- fastapi
- mysql
- uvicorn
- sqlalchemy
- alembic
- pymysql
- pydantic
- python-dotenv

See `backend/requirements.txt` for the full list.

## API Endpoints

### Categories

- `POST   /categories/` — Create a new category
- `GET    /categories/` — List all categories
- `GET    /categories/{id}` — Get a category by ID

### Products

- `POST   /products/` — Create a new product
- `GET    /products/` — List all products
- `GET    /products/{id}` — Get a product by ID

### Inventory

- `GET    /inventory/` — List inventory items
- `GET    /inventory/low-stock` — List items at/below reorder threshold
- `GET    /inventory/history` — List inventory history
- `GET    /inventory/{product_id}` — Get inventory for a product
- `PATCH  /inventory/{product_id}` — Update inventory for a product
- `POST   /inventory/{product_id}/history` — Record inventory change

### Sales

- `POST   /sales/` — Create a new sale (with items)
- `GET    /sales/` — List/filter sales
- `GET    /sales/{id}` — Get a sale by ID
- `GET    /sales/stats` — Revenue summary (daily/weekly/monthly/yearly)
- `GET    /sales/compare` — Compare revenue between two periods
- `GET    /sales/by-product/{product_id}` — List sales for a product
- `GET    /sales/by-category/{category_id}` — List sales for a category

### Sale Items

- `GET    /sale-items/` — List sale items (filter by product or sale)

## Development Notes

- All endpoints return JSON.
- Interactive API docs available at `/docs` (Swagger UI) and `/redoc`.
- Database migrations managed with Alembic.
