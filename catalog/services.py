from django.core.mail import send_mail
from django.conf import settings


def send_email(record):
    send_mail(
        f'100 просмотров: {record}',
        f'100 просмотров записи {record}',
        settings.EMAIL_HOST_USER,
        ['gadjka@mail.ru']

    )
