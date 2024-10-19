import os
import time
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_comparison.djangoproject.settings')
django.setup()

from djangoproject.models import Product

N = 1000


def insert_records():
    start_time = time.time()
    for i in range(N):
        Product.objects.create(
            name=f'Product {i}',
            price=i * 10.0,
            stock=i,
            description=f'Description {i}'
        )
    end_time = time.time()
    with open('output.txt', 'a', encoding='cp1251') as f:
        f.write(f'Вставка {N} записей заняла {end_time - start_time:.2f} секунд\n')


def read_records():
    start_time = time.time()
    products = Product.objects.all()
    for product in products:
        pass
    end_time = time.time()
    with open('output.txt', 'a', encoding='cp1251') as f:
        f.write(f'Чтение {N} записей заняло {end_time - start_time:.2f} секунд\n')


def update_records():
    start_time = time.time()
    products = Product.objects.all()
    for product in products:
        product.price += 1
        product.save()
    end_time = time.time()
    with open('output.txt', 'a', encoding='cp1251') as f:
        f.write(f'Обновление {N} записей заняло {end_time - start_time:.2f} секунд\n')


def delete_records():
    start_time = time.time()
    Product.objects.all().delete()
    end_time = time.time()
    with open('output.txt', 'a', encoding='cp1251') as f:
        f.write(f'Удаление {N} записей заняло {end_time - start_time:.2f} секунд\n')



insert_records()
read_records()
update_records()
delete_records()