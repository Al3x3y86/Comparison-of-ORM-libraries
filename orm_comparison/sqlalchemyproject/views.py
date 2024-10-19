from flask import Flask, request, render_template, redirect
from sqlalchemyproject.db_setup import session
from sqlalchemyproject.models import Product

app = Flask(__name__)


@app.route('/')
def product_list():
    products = session.query(Product).all()
    return render_template('product_list.html', products=products)


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
