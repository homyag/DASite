from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactRequest(models.Model):
    """Модель для хранения заявок обратной связи."""

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('Новая')
        IN_PROGRESS = 'in_progress', _('В обработке')
        COMPLETED = 'completed', _('Завершена')
        CANCELED = 'canceled', _('Отменена')

    class ServiceChoices(models.TextChoices):
        WEB_DEVELOPMENT = 'web_development', _('Веб-разработка')
        MOBILE_DEVELOPMENT = 'mobile_development', _('Мобильная разработка')
        DESIGN = 'design', _('Дизайн')
        SEO = 'seo', _('SEO оптимизация')
        MARKETING = 'marketing', _('Маркетинг')
        OTHER = 'other', _('Другое')

    # Основная информация
    name = models.CharField(_('Имя'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Телефон'), max_length=17)
    service = models.CharField(
        _('Услуга'),
        max_length=50,
        choices=ServiceChoices.choices,
        default=ServiceChoices.WEB_DEVELOPMENT
    )
    message = models.TextField(_('Сообщение'))

    # Статус и даты
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    # # Honeypot поле (не выводится в админке, используется для отлова спам-ботов)
    # website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"