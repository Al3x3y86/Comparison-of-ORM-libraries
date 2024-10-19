import asyncio
import time
from tortoise import Tortoise
from tortoiseproject.models import Product


import sys
sys.path.append('C:/Users/Кузьминых/PycharmProjects/Diploma/DProject/orm_comparison')

N = 1000


async def init():
    try:
        print("Инициализация базы данных...")
        await Tortoise.init(
            db_url='sqlite://tortoise_db.sqlite3',
            modules={'models': ['tortoiseproject.models']}
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


async def insert_records():
    start_time = time.time()
    try:
        print("Начинаем вставку записей...")
        for i in range(N):
            await Product.create(
                name=f'Product {i}',
                price=i * 10.0,
                stock=i,
                description=f'Description {i}'
            )
        end_time = time.time()
        with open('output_tortoise.txt', 'a', encoding='utf-8') as f:
            f.write(f'Вставка {N} записей заняла {end_time - start_time:.2f} секунд\n')
        print("Вставка завершена.")
    except Exception as e:
        print(f"Ошибка при вставке записей: {e}")


async def read_records():
    start_time = time.time()
    try:
        print("Начинаем чтение записей...")
        products = await Product.all()
        for product in products:
            pass
        end_time = time.time()
        with open('output_tortoise.txt', 'a', encoding='utf-8') as f:
            f.write(f'Чтение {N} записей заняло {end_time - start_time:.2f} секунд\n')
        print("Чтение завершено.")
    except Exception as e:
        print(f"Ошибка при чтении записей: {e}")


async def update_records():
    start_time = time.time()
    try:
        print("Начинаем обновление записей...")
        products = await Product.all()
        for product in products:
            product.price += 1
            await product.save()
        end_time = time.time()
        with open('output_tortoise.txt', 'a', encoding='utf-8') as f:
            f.write(f'Обновление {N} записей заняло {end_time - start_time:.2f} секунд\n')
        print("Обновление завершено.")
    except Exception as e:
        print(f"Ошибка при обновлении записей: {e}")


async def delete_records():
    start_time = time.time()
    try:
        print("Начинаем удаление записей...")
        await Product.all().delete()
        end_time = time.time()
        with open('output_tortoise.txt', 'a', encoding='utf-8') as f:
            f.write(f'Удаление {N} записей заняло {end_time - start_time:.2f} секунд\n')
        print("Удаление завершено.")
    except Exception as e:
        print(f"Ошибка при удалении записей: {e}")


async def run_tests():
    await init()
    await insert_records()
    await read_records()
    await update_records()
    await delete_records()

if __name__ == '__main__':
    try:
        print("Запуск тестов...")
        asyncio.run(run_tests())
        print("Тесты завершены.")
    except Exception as e:
        print(f"Ошибка при выполнении тестов: {e}")
