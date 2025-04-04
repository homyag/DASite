import logging
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse

from .forms import ContactForm

logger = logging.getLogger(__name__)


def contact_submit_view(request):
    """Обработчик формы обратной связи."""
    # Получаем URL страницы, с которой пришел запрос
    referer = request.META.get('HTTP_REFERER', '')

    # Проверяем, является ли запрос AJAX-запросом
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Проверка на спам через honeypot-поле
        if request.POST.get('website'):
            logger.warning(
                f"Spam detected: honeypot field filled from {request.META.get('REMOTE_ADDR')}")
            # Имитируем успех для бота, но не сохраняем форму
            if is_ajax:
                return JsonResponse({'success': True})
            else:
                return redirect('contact_success')

        if form.is_valid():
            try:
                # Сохраняем форму и получаем объект контакта
                contact = form.save()

                # Логирование для аналитики
                logger.info(
                    f"Form submitted: {contact.id} from {request.META.get('REMOTE_ADDR')}")

                # Отправка уведомления администратору
                subject = f'Новая заявка от {contact.name}'
                html_message = render_to_string(
                    'contacts/email/admin_notification.html', {
                        'contact': contact,
                        'site_url': f"{request.scheme}://{request.get_host()}"
                    })
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [
                    settings.DEFAULT_FROM_EMAIL]  # На email администратора

                # Отправляем email администратору
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                    fail_silently=False,
                )

                # Отправка подтверждения клиенту
                subject = 'Спасибо за ваше обращение в DAAgency'
                html_message = render_to_string(
                    'contacts/email/client_notification.html', {
                        'contact': contact
                    })
                plain_message = strip_tags(html_message)
                to_email = [contact.email]

                # Отправляем email клиенту
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                    fail_silently=False,
                )

                # Если запрос через AJAX, возвращаем JSON-ответ
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'
                    })

                # Устанавливаем сообщение об успехе
                messages.success(request,
                                 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')

                # Перенаправляем на страницу успеха
                return redirect('contact_success')

            except Exception as e:
                # Логируем ошибку для диагностики
                logger.error(f"Ошибка при отправке email: {e}")

                # Если запрос через AJAX, возвращаем JSON-ответ с ошибкой
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону.'
                    })

                # Устанавливаем сообщение об ошибке
                messages.error(request,
                               'Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону.')

                # Возвращаем пользователя на страницу с формой
                if referer:
                    return redirect(referer)
                return redirect(
                    'home')  # Если referer недоступен, перенаправляем на главную
        else:
            # Если форма не валидна
            # Для AJAX-запроса возвращаем ошибки валидации в формате JSON
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors': json.loads(form.errors.as_json())
                })

            # Если форма не валидна, добавляем сообщение об ошибке
            messages.error(request,
                           'Пожалуйста, проверьте правильность заполнения формы.')

            # Возвращаем пользователя на страницу с формой с заполненными данными
            if referer:
                # Сохраняем данные формы в сессии для восстановления после редиректа
                request.session['form_data'] = request.POST
                return redirect(referer)

            # Если referer недоступен, отображаем форму на текущей странице
            return render(request, 'contacts/contact.html', {'form': form})
    else:
        # GET запрос - просто перенаправляем на главную
        return redirect('home')


def contact_success_view(request):
    """Страница успешной отправки формы."""
    return render(request, 'contacts/contact_success.html')


def contact_view(request):
    return render(request, 'contacts/contact.html')
