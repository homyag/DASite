# core/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class ContactRequest(models.Model):
    """Модель для хранения заявок обратной связи."""

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('Новая')
        IN_PROGRESS = 'in_progress', _('В обработке')
        COMPLETED = 'completed', _('Завершена')
        CANCELED = 'canceled', _('Отменена')

    class ServiceChoices(models.TextChoices):
        SEO = 'seo', _('SEO-продвижение')
        EMAIL = 'email', _('Email-маркетинг')
        CONTENT = 'content', _('Контент-маркетинг')
        SMM = 'smm', _('SMM-продвижение')
        ORM = 'orm', _('Репутационный маркетинг')
        PPC = 'ppc', _('PPC-реклама')
        COMPLEX = 'complex', _('Комплексное продвижение')
        OTHER = 'other', _('Другое')

    # Основная информация
    name = models.CharField(_('Имя'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Телефон'), max_length=32)
    service = models.CharField(
        _('Услуга'),
        max_length=50,
        choices=ServiceChoices.choices,
        default=ServiceChoices.OTHER
    )
    message = models.TextField(_('Сообщение'))

    # Дополнительные поля для форм
    company = models.CharField(_('Компания'), max_length=100, blank=True, null=True)
    website = models.URLField(_('Сайт'), blank=True, null=True)
    budget = models.CharField(_('Бюджет'), max_length=100, blank=True, null=True)
    tariff = models.CharField(_('Тариф'), max_length=100, blank=True, null=True)

    # Информация о запросе
    source = models.CharField(_('Источник заявки'), max_length=200, blank=True, null=True,
                              help_text=_('Страница, с которой была отправлена форма'))
    ip_address = models.GenericIPAddressField(_('IP-адрес'), blank=True, null=True)
    user_agent = models.TextField(_('User-Agent'), blank=True, null=True)

    # Статус и даты
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    # Поля для администрирования
    admin_notes = models.TextField(_('Заметки администратора'), blank=True, null=True)
    assigned_to = models.CharField(_('Ответственный'), max_length=100, blank=True, null=True)

    # Honeypot поле (не выводится в админке, используется для отлова спам-ботов)
    website_honeypot = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"


class Profile(models.Model):
    """Расширенный профиль пользователя с дополнительной информацией"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True,
                              verbose_name="Фото")
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    position = models.CharField(max_length=100, blank=True, null=True,
                                verbose_name="Должность")
    company = models.CharField(max_length=100, blank=True, null=True,
                               verbose_name="Компания")

    # Социальные сети и контакты
    linkedin_url = models.URLField(max_length=200, blank=True, null=True,
                                   verbose_name="LinkedIn")
    twitter_url = models.URLField(max_length=200, blank=True, null=True,
                                  verbose_name="Twitter")
    github_url = models.URLField(max_length=200, blank=True, null=True,
                                 verbose_name="GitHub")
    website_url = models.URLField(max_length=200, blank=True, null=True,
                                  verbose_name="Веб-сайт")

    # Дополнительные поля для экспертизы
    expertise = models.ManyToManyField('Expertise', blank=True,
                                       verbose_name="Области экспертизы")
    years_experience = models.PositiveIntegerField(default=0,
                                                   verbose_name="Лет опыта")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.get_full_name() or self.user.username}"


class Expertise(models.Model):
    """Модель для хранения областей экспертизы авторов"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор")

    class Meta:
        verbose_name = "Область экспертизы"
        verbose_name_plural = "Области экспертизы"

    def __str__(self):
        return self.name



class Newsletter(models.Model):
    """Модель для хранения подписчиков рассылки."""
    email = models.EmailField(verbose_name="Email", unique=True)
    is_active = models.BooleanField(verbose_name="Активен", default=True)
    created_at = models.DateTimeField(verbose_name="Дата подписки", auto_now_add=True)

    class Meta:
        verbose_name = "Подписчик рассылки"
        verbose_name_plural = "Подписчики рассылки"
        ordering = ['-created_at']

    def __str__(self):
        return self.email


# Автоматическое создание профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()