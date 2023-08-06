from django.core.management import BaseCommand
from catalog.models import Category
from catalog.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Удаление всей информации из БД"""
        all_products = Product.objects.all()
        for item in all_products:
            item.delete()

        all_category = Category.objects.all()
        for item_c in all_category:
            item_c.delete()
        """Заполнение БД"""
        category_list = [
            {'id': '1', 'name': 'Смартфоны', 'description': 'общение'},
            {'id': '2', 'name': 'Ноутбуки', 'description': 'laptop'},
            {'id': '3', 'name': 'Канцтовары', 'description': 'бумага и пишущие принадлежности'}

        ]
        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )
        Category.objects.bulk_create(category_for_create)

        product_list = [
            {'id': '1', 'name': 'Бумага SVETOCOPY', 'description': 'A4, Classic, белая',
             'category': Category.objects.get(pk=3), 'price': '1850'},
            {'id': '2', 'name': 'Ручка Erich Krause', 'description': 'шариковая, автоматическая, синяя',
             'category': Category.objects.get(pk=3), 'price': '180'},
            {'id': '3', 'name': 'Смартфон Xiaomi Poco', 'description': 'X5 Pro, черный',
             'category': Category.objects.get(pk=1), 'price': '31000'},
            {'id': '4', 'name': 'Смартфон Apple', 'description': 'iPhone 14, голубой',
             'category': Category.objects.get(pk=1), 'price': '86900'},
            {'id': '5', 'name': 'Ноутбук ASUS', 'description': 'Intel Core i7, NVIDIA GeForce MX330',
             'category': Category.objects.get(pk=2), 'price': '54900'},
            {'id': '6', 'name': 'Ноутбук Huawei', 'description': 'Intel Core i5, Intel UHD Graphics',
             'category': Category.objects.get(pk=2), 'price': '76900'},
        ]
        products_for_create = []
        for product_item in product_list:
            products_for_create.append(
                Product(**product_item)
            )
        Product.objects.bulk_create(products_for_create)
