from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from catalog.models import Category


def send_email(record):
    send_mail(
        f'100 просмотров: {record}',
        f'100 просмотров записи {record}',
        settings.EMAIL_HOST_USER,
        ['gadjka@mail.ru']

    )


def get_categories(category_pk):
    if settings.CACHE_ENABLED:
        key = f'category_list_{category_pk}'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.filter(category_id=category_pk)
            cache.set(key, category_list)
    else:
        category_list = Category.objects.filter(category_id=category_pk)

    return category_list

