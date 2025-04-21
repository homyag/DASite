from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import traceback

from .forms import NewsletterForm
from .models import Newsletter

# Настраиваем логгер
logger = logging.getLogger(__name__)


@require_POST
def newsletter_subscribe(request):
    """Обработка формы подписки на рассылку."""
    # Получаем URL страницы, с которой пришел запрос
    referer = request.META.get('HTTP_REFERER', '')

    # Проверяем, является ли запрос AJAX-запросом
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    form = NewsletterForm(request.POST)

    if form.is_valid():
        try:
            # Сохраняем подписчика
            subscriber = form.save()

            # Логируем информацию для отладки
            logger.info(f"Подписчик сохранен: {subscriber.email}")
            logger.info(f"Настройки EMAIL_HOST: {settings.EMAIL_HOST}")
            logger.info(f"Настройки EMAIL_PORT: {settings.EMAIL_PORT}")
            logger.info(f"Настройки EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            logger.info(f"Настройки EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
            logger.info(f"Настройки EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")

            # Отправляем подтверждение подписки
            try:
                subject = 'Подтверждение подписки на рассылку Boldrise Agency'
                html_message = render_to_string('core/email/subscription_confirmation.html', {
                    'email': subscriber.email,
                })
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [subscriber.email]

                logger.info(f"Попытка отправить письмо на {to_email} от {from_email}")

                # Отправка с более подробным логированием ошибок
                send_result = send_mail(
                    subject,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                    fail_silently=False,  # Изменено на False для получения полных ошибок
                )

                logger.info(f"Результат отправки письма: {send_result}")

                # Успешное сообщение
                success_message = "Спасибо за подписку! Мы отправили вам письмо для подтверждения."

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': success_message
                    })

                messages.success(request, success_message)

            except Exception as e:
                # Подробное логирование ошибки с трассировкой стека
                logger.error(f"Ошибка при отправке подтверждения подписки: {str(e)}")
                logger.error(traceback.format_exc())

                error_message = f"Ошибка при отправке подтверждения: {str(e)}"

                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': "Вы успешно подписаны, но возникла проблема с отправкой подтверждения."
                    })

                # В любом случае подписка создана, поэтому успешное сообщение с предупреждением
                messages.success(request, "Вы успешно подписаны на рассылку!")
                messages.warning(request, "Однако возникла проблема с отправкой письма-подтверждения.")

        except Exception as e:
            logger.error(f"Ошибка при создании подписки: {str(e)}")
            logger.error(traceback.format_exc())

            error_message = f"Произошла ошибка при подписке: {str(e)}"

            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                })

            messages.error(request, error_message)
    else:
        # Если форма невалидна
        logger.warning(f"Форма подписки невалидна: {form.errors}")

        if is_ajax:
            # Собираем все ошибки из формы
            errors = dict([(key, [error for error in field_errors])
                           for key, field_errors in form.errors.items()])

            # Для удобства интерфейса берем первую ошибку для отображения
            first_error = next(iter(form.errors.values()))[0] if form.errors else "Некорректные данные формы."

            return JsonResponse({
                'success': False,
                'message': first_error,
                'errors': errors
            })

        # Добавляем все ошибки в сообщения для отображения на странице
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    # Возвращаемся на предыдущую страницу
    if referer:
        return redirect(referer)

    # Если referer недоступен, перенаправляем на главную
    return redirect('home')