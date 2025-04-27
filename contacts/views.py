import logging
import json
import traceback

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.urls import resolve, reverse

from contacts.forms import ContactForm
from core.models import ContactRequest

logger = logging.getLogger(__name__)


def contact_submit_view(request):
    """Обработчик формы обратной связи с подробным логированием для отладки."""
    # Получаем URL страницы, с которой пришел запрос
    referer = request.META.get('HTTP_REFERER', '')

    # Логируем все данные запроса для отладки
    logger.info(f"Получен запрос на contact_submit_view:")
    logger.info(f"Method: {request.method}")
    logger.info(f"Referer: {referer}")
    logger.info(f"Is AJAX: {'XMLHttpRequest' in request.headers.get('X-Requested-With', '')}")
    logger.info(f"Content-Type: {request.headers.get('Content-Type', '')}")

    if request.method == 'POST':
        logger.info(f"POST-данные: {request.POST}")

        try:
            # Создаем экземпляр формы с POST-данными
            form = ContactForm(request.POST)
            logger.info(f"Форма создана: {form}")

            # Проверка на спам через honeypot-поле
            if request.POST.get('website'):
                logger.warning(f"Spam detected: honeypot field filled from {request.META.get('REMOTE_ADDR')}")
                # Имитируем успех для бота, но не сохраняем форму
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('contact_success')

            # Проверяем валидность формы
            if form.is_valid():
                # Сохраняем форму в базу данных
                contact = form.save(commit=False)
                # Определяем страницу, с которой была отправлена форма
                source_page = resolve(referer.replace(request.build_absolute_uri('/'), '/')).url_name if referer else 'unknown'
                contact.source = source_page
                contact.save()
                
                # Отправляем уведомления
                try:
                    send_admin_notification(request, contact, source_page)
                    send_client_confirmation(contact)
                except Exception as e:
                    logger.error(f"Ошибка при отправке уведомлений: {str(e)}")
                    # Продолжаем выполнение, так как форма уже сохранена

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.'
                    })
                else:
                    messages.success(request, 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
                    return redirect('contact_success')
            else:
                logger.warning(f"Ошибки валидации формы: {form.errors}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': form.errors
                    }, status=400)
                else:
                    messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
                    return redirect('contact')

        except Exception as e:
            logger.error(f"Ошибка при сохранении формы: {str(e)}")
            logger.error(traceback.format_exc())
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте позже.'
                }, status=500)
            else:
                messages.error(request, 'Произошла ошибка при отправке формы. Пожалуйста, попробуйте позже.')
                return redirect('contact')

    # Если метод не POST
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def send_admin_notification(request, contact, source_page):
    """Отправка уведомления администратору о новой заявке."""
    subject = f'Новая заявка от {contact.name} - {source_page}'
    context = {
        'contact': contact,
        'site_url': f"{request.scheme}://{request.get_host()}",
        'source_page': source_page,
        'admin_url': f"{request.scheme}://{request.get_host()}/admin/core/contactrequest/{contact.id}/",
    }

    # Полный путь к шаблону для отладки
    template_path = 'contacts/email/admin_notification.html'
    logger.info(f"Используем шаблон для админа: {template_path}")

    try:
        html_message = render_to_string(template_path, context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = getattr(settings, 'EMAIL_ADMIN', settings.DEFAULT_FROM_EMAIL)  # Используем настройку EMAIL_ADMIN

        logger.info(f"Отправка письма администратору:")
        logger.info(f"От: {from_email}")
        logger.info(f"Кому: {to_email}")
        logger.info(f"Тема: {subject}")

        # Создаем сообщение
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [to_email],
        )

        # Добавляем HTML-версию
        email.attach_alternative(html_message, "text/html")

        # Отправляем сообщение
        email.send(fail_silently=False)

        logger.info(f"Admin notification sent to {to_email} for contact request #{contact.id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке письма администратору: {e}")
        logger.error(traceback.format_exc())
        raise


def send_client_confirmation(contact):
    """Отправка подтверждения клиенту о получении заявки."""
    subject = 'Спасибо за ваше обращение в Boldrise Agency'

    # Настройка контекста для шаблона
    context = {
        'contact': contact,
        'company_email': settings.EMAIL_HOST_USER,
        'company_phone': '+7 (999) 999-99-99',  # TODO: Заменить на реальный телефон
        'company_telegram': 'https://t.me/boldrise',  # TODO: Заменить на реальную ссылку
        'company_vk': 'https://vk.com/boldrise',  # TODO: Заменить на реальную ссылку
    }

    # Полный путь к шаблону для отладки
    template_path = 'contacts/email/client_notification.html'
    logger.info(f"Используем шаблон для клиента: {template_path}")

    try:
        html_message = render_to_string(template_path, context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = contact.email

        logger.info(f"Отправка письма клиенту:")
        logger.info(f"От: {from_email}")
        logger.info(f"Кому: {to_email}")
        logger.info(f"Тема: {subject}")

        # Создаем сообщение
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [to_email],
        )

        # Добавляем HTML-версию
        email.attach_alternative(html_message, "text/html")

        # Отправляем сообщение
        email.send(fail_silently=False)

        logger.info(f"Client confirmation sent to {to_email} for contact request #{contact.id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке письма клиенту: {e}")
        logger.error(traceback.format_exc())
        raise


def contact_success_view(request):
    """Страница успешной отправки формы."""
    return render(request, 'contacts/contact_success.html')


def contact_view(request):
    return render(request, 'contacts/contact.html')
