
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 1200.50, "in_stock": True},
    {"id": 2, "name": "Phone", "price": 500.0, "in_stock": True},
    {"id": 3, "name": "Tablet", "price": 300.0, "in_stock": True},
]


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def create_product(product: Product):
    new_product = {
        "id": max(p["id"] for p in products) + 1,
        **product.model_dump()
    }

    products.append(new_product)

    return {
        "message": "Product created successfully",
        "product": new_product
    }
