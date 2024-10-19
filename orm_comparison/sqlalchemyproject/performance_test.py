import time
from sqlalchemyproject.db_setup import session
from sqlalchemyproject.models import Product


N = 1000


def insert_records():
    start_time = time.time()
    for i in range(N):
        product = Product(
            name=f'Product {i}',
            price=i * 10.0,
            stock=i,
            description=f'Description {i}'
        )
        session.add(product)
    session.commit()
    end_time = time.time()
    with open('output_sqlalchemy.txt', 'a', encoding='cp1251') as f:
        f.write(f'Вставка {N} записей заняла {end_time - start_time:.2f} секунд\n')


insert_records()


def read_records():
    start_time = time.time()
    products = session.query(Product).all()
    for product in products:
        pass
    end_time = time.time()
    with open('output_sqlalchemy.txt', 'a', encoding='cp1251') as f:
        f.write(f'Чтение {N} записей заняло {end_time - start_time:.2f} секунд\n')


read_records()


def update_records():
    start_time = time.time()
    products = session.query(Product).all()
    for product in products:
        product.price += 1
        session.add(product)
    session.commit()
    end_time = time.time()
    with open('output_sqlalchemy.txt', 'a', encoding='cp1251') as f:
        f.write(f'Обновление {N} записей заняло {end_time - start_time:.2f} секунд\n')


update_records()


def delete_records():
    start_time = time.time()
    session.query(Product).delete()
    session.commit()
    end_time = time.time()
    with open('output_sqlalchemy.txt', 'a', encoding='cp1251') as f:
        f.write(f'Удаление {N} записей заняло {end_time - start_time:.2f} секунд\n')


delete_records()
