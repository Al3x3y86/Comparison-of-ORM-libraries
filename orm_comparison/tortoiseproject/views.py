from fastapi import FastAPI
from orm_comparison.tortoiseproject.models import Product
from orm_comparison.tortoiseproject.db_setup import init
from tortoise import Tortoise

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init()


@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


@app.get("/")
async def product_list():
    return await Product.all()


@app.post("/create")
async def product_create(name: str, price: float, stock: int, description: str):
    product = await Product.create(name=name, price=price, stock=stock, description=description)
    return product


@app.put("/update/{product_id}")
async def product_update(product_id: int, name: str, price: float, stock: int, description: str):
    product = await Product.filter(id=product_id).first()
    if not product:
        return {"error": "Product not found"}

    product.name = name
    product.price = price
    product.stock = stock
    product.description = description
    await product.save()
    return product


@app.delete("/delete/{product_id}")
async def product_delete(product_id: int):
    product = await Product.filter(id=product_id).first()
    if not product:
        return {"error": "Product not found"}

    await product.delete()
    return {"message": f"Product with id {product_id} has been deleted"}


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    product = await Product.filter(id=product_id).first()
    if not product:
        return {"error": "Product not found"}
    return product
