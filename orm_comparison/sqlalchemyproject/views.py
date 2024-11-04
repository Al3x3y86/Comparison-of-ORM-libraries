from flask import Flask, request, render_template, redirect
from sqlalchemyproject.db_setup import session
from sqlalchemyproject.models import Product
from sqlalchemy import func

app = Flask(__name__)

@app.route('/')
def product_list():
    # Все товары
    query = session.query(Product)

    # Фильтр по цене
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    if min_price and max_price:
        query = query.filter(Product.price >= min_price, Product.price <= max_price)

    # Фильтр по количеству на складе
    sort_by_stock = request.args.get('sort')
    if sort_by_stock == 'stock':
        query = query.order_by(Product.stock)

    # Фильтр по описанию
    description_filter = request.args.get('description')
    if description_filter:
        query = query.filter(Product.description.ilike(f'%{description_filter}%'))

    # Список товаров
    products = query.all()

    # Средняя цена
    average_price = session.query(func.avg(Product.price)).scalar()

    return render_template('product_list.html', products=products, average_price=average_price)


@app.route('/create', methods=['GET', 'POST'])
def product_create():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            price=request.form['price'],
            stock=request.form['stock'],
            description=request.form['description']
        )
        session.add(product)
        session.commit()
        return redirect('/')
    return render_template('product_create.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def product_update(id):
    product = session.query(Product).get(id)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.description = request.form['description']
        session.commit()
        return redirect('/')
    return render_template('product_update.html', product=product)


@app.route('/delete/<int:id>', methods=['POST'])
def product_delete(id):
    product = session.query(Product).get(id)
    if not product:
        return "Product not found", 404

    session.delete(product)
    session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
