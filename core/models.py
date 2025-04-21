# core/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('processing', 'В обработке'),
        ('completed', 'Обработана'),
        ('canceled', 'Отменена'),
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    service = models.CharField(max_length=100, blank=True, null=True,
                               verbose_name="Услуга")
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at.strftime('%d.%m.%Y')})"


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