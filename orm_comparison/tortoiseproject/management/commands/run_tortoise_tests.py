from django.core.management.base import BaseCommand
import asyncio
from tortoiseproject.performance_test import run_tests

class Command(BaseCommand):
    help = 'Запуск тестов Tortoise ORM'

    def handle(self, *args, **kwargs):
        asyncio.run(run_tests())
