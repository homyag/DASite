# Создайте файл test_email.py в корне проекта
import os
import sys
import django

# Настраиваем окружение Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DASite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email():
    subject = 'Тестовое письмо от Django'
    message = 'Это тестовое письмо для проверки настроек SMTP.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['адрес_получателя@example.com']  # Замените на реальный адрес

    print(f"Отправка письма от {from_email} на {recipient_list}")
    print(f"Настройки EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"Настройки EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"Настройки EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"Настройки EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"Настройки EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")

    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f"Результат отправки: {result}")
        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_email()

# Запустите этот скрипт из командной строки:
# python test_email.py