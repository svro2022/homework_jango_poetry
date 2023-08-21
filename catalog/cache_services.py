from catalog.models import Category
from django.core.cache import cache
from config.settings import CACHE_ENABLED


def get_categories():
    '''Получаем категории'''
    categories = Category.objects.all()
    return categories


def categories_cache():
    '''Кеширование списка, полученных категорий'''
    if CACHE_ENABLED:
        key = 'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = get_categories()
            cache.set(key, categories_list)

        return categories_list

