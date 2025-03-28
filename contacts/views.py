# contacts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Отправка уведомления администратору
            subject = f'Новая заявка от {contact.name}'
            html_message = render_to_string(
                'contacts/email/admin_notification.html', {
                    'contact': contact
                })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]  # На email администратора

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
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [contact.email]

            send_mail(
                subject,
                plain_message,
                from_email,
                to_email,
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(request,
                             'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact.html', {'form': form})


def contact_success_view(request):
    return render(request, 'contacts/contact_success.html')