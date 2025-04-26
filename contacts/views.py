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
            is_valid = form.is_valid()
            logger.info(f"Форма валидна: {is_valid}")

            if not is_valid:
                logger.warning(f"Ошибки валидации формы: {form.errors}")

                # Для AJAX-запроса возвращаем ошибки валидации
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': json.loads(form.errors.as_json())
                    })

                # Если форма не валидна, добавляем сообщение об ошибке
                messages.error(request, 'Пожалуйста, проверьте правильность заполнения формы.')

                # Возвращаем на предыдущую страницу
                if referer:
                    return redirect(referer)
                return render(request, 'contacts/contact.html', {'form': form})

            # Если форма валидна, сохраняем данные
            try:
                # Определяем источник формы
                source_page = "Неизвестная страница"
                if referer:
                    if '/service/' in referer:
                        service_name = referer.split('/service/')[-1].split('/')[0]
                        if service_name:
                            source_page = f"Страница услуги: {service_name}"
                    elif '/contact' in referer:
                        source_page = "Страница контактов"
                    elif referer.endswith('/'):
                        source_page = "Главная страница"

                # Сохраняем заявку в базу данных
                contact = form.save()

                # Добавляем информацию об источнике
                contact.source = source_page
                contact.ip_address = request.META.get('REMOTE_ADDR', '')
                contact.user_agent = request.META.get('HTTP_USER_AGENT', '')
                contact.save()

                logger.info(f"Заявка успешно сохранена в БД: ID={contact.id}, Источник={source_page}")

                # Отправляем email-уведомления
                try:
                    # Отправка уведомления администратору
                    send_admin_notification(request, contact, source_page)
                    logger.info(f"Email администратору успешно отправлен")

                    # Отправка подтверждения клиенту
                    send_client_confirmation(contact)
                    logger.info(f"Email клиенту успешно отправлен")
                except Exception as email_error:
                    logger.error(f"Ошибка при отправке email: {email_error}")
                    logger.error(traceback.format_exc())

                # Для AJAX-запроса возвращаем JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.',
                        'redirect_url': reverse('contact_success')
                    })

                # Устанавливаем сообщение об успехе
                messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')

                # Перенаправляем на страницу успеха
                return redirect('contact_success')

            except Exception as save_error:
                logger.error(f"Ошибка при сохранении формы: {save_error}")
                logger.error(traceback.format_exc())

                # Если запрос через AJAX, возвращаем ошибку
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Произошла ошибка при обработке заявки. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону.'
                    })

                messages.error(request,
                               'Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону.')

                if referer:
                    return redirect(referer)
                return redirect('home')

        except Exception as form_error:
            logger.error(f"Общая ошибка обработки формы: {form_error}")
            logger.error(traceback.format_exc())

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Произошла ошибка при обработке запроса.'
                })

            messages.error(request, 'Произошла ошибка при обработке запроса.')

            if referer:
                return redirect(referer)
            return redirect('home')
    else:
        # GET запрос - просто перенаправляем на главную
        logger.warning(f"Получен GET-запрос вместо POST в contact_submit_view")
        return redirect('home')


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
