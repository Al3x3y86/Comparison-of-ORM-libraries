from fastapi import FastAPI, Query
from orm_comparison.tortoiseproject.models import Product
from orm_comparison.tortoiseproject.db_setup import init
from tortoise import Tortoise
from tortoise.functions import Avg

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init()


@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


@app.get("/")
async def product_list(
        min_price: float = Query(None, description="Минимальная цена"),
        max_price: float = Query(None, description="Максимальная цена"),
        description: str = Query(None, description="Описание товара"),
        sort_by_stock: bool = Query(False, description="Сортировать по количеству на складе")
        ):
    query = Product.all()

    # Минимальная цена
    if min_price is not None:
        query = query.filter(price__gte=min_price)

    # Максимальная цена
    if max_price is not None:
        query = query.filter(price__lte=max_price)

    # Фильтр по описанию
    if description:
        query = query.filter(description__icontains=description)

    # Фильтр по количеству на складе
    if sort_by_stock:
        query = query.order_by('stock')

    # Получаем товары
    products = await query

    # Средняя цена
    average_price_result = await Product.annotate(average_price=Avg("price")).first()
    average_price = average_price_result.average_price if average_price_result else 0

    return {"products": products, "average_price": average_price}


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
