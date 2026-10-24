
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

products = [
    {"id": 1, "name": "Keyboard", "price": 1200.50, "in_stock": True},
    {"id": 2, "name": "Phone", "price": 500.0, "in_stock": True},
    {"id": 3, "name": "Tablet", "price": 300.0, "in_stock": True},
]


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None  
    in_stock: bool | None = None


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=status.HTTP_201_CREATED)
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

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:
            updated_product = {
                "id": product_id,
                **product.model_dump()
            }

            products[index] = updated_product
            return {
                "message": "Product updated successfully",
                "product": updated_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.patch("/products/{product_id}")
def patch_product(product_id: int, updates: ProductUpdate):
    for product in products:
        if product["id"] == product_id:
            product.update(
                updates.model_dump(exclude_unset=True)
            )
            return {
                "message": "Product updated successfully",
                "product": product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(index)
            return {
                "message": "Product deleted successfully",
                "product": deleted_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )