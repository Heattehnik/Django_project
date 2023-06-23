from django.core.management import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):
    help = 'Команда для очистки таблицы и заполнения данными'

    def handle(self, *args, **options):
        # Очистка таблицы категорий от данных
        Category.objects.all().delete()
        # Список категорий для добавления
        categories_list = [
            {"name": "Резиновые уточки", "description": "Резиновые уточки для ванной"},
            {"name": "Балалайки", "description": "Инструменты"},
            {"name": "Надувные матрасы", "description": "Отличные матрасы для здорового сна"},
            {"name": "Спортивный инвентарь", "description": "В здоровом теле, здоровый дух"},
                           ]

        categories_to_create = []
        for category in categories_list:
            categories_to_create.append(Category(**category))

        Category.objects.bulk_create(categories_to_create)

