# services/models.py
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class Service(models.Model):
    """Модель для хранения информации об услугах агентства"""
    name = models.CharField('Название услуги', max_length=100)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)
    title = models.CharField('Заголовок страницы', max_length=200)
    description = models.TextField('Краткое описание', max_length=500)
    full_description = HTMLField('Полное описание')
    # Добавляем поле для хранения SVG-иконки
    icon_svg = models.TextField('SVG-иконка', blank=True, help_text="Вставьте SVG-код иконки")
    icon = models.CharField('Иконка (класс или SVG)', max_length=500, blank=True)
    image = models.ImageField('Изображение услуги', upload_to='services/', blank=True)
    is_active = models.BooleanField('Активно', default=True)
    is_featured = models.BooleanField('Отображать на главной', default=True)
    meta_title = models.CharField('Meta Title', max_length=200, blank=True)
    meta_description = models.TextField('Meta Description', max_length=500, blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'name']


class ServiceFeature(models.Model):
    """Модель для хранения особенностей/пунктов услуг"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField('Заголовок пункта', max_length=200)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Особенность услуги'
        verbose_name_plural = 'Особенности услуг'
        ordering = ['service', 'order']


class ServiceBenefit(models.Model):
    """Модель для хранения преимуществ услуг"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='benefits')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    icon = models.CharField('Иконка (класс или SVG)', max_length=500,
                            blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Преимущество услуги'
        verbose_name_plural = 'Преимущества услуг'
        ordering = ['order']


class ServiceProcess(models.Model):
    """Модель для хранения этапов процесса работы"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='processes')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    icon = models.CharField('Иконка (класс или SVG)', max_length=500,
                            blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Этап процесса'
        verbose_name_plural = 'Этапы процесса'
        ordering = ['order']


class FAQ(models.Model):
    """Модель для хранения часто задаваемых вопросов"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='faqs', null=True, blank=True)
    question = models.CharField('Вопрос', max_length=500)
    answer = HTMLField('Ответ')
    is_common = models.BooleanField('Общий вопрос', default=False,
                                    help_text='Отметьте, если вопрос относится ко всем услугам')
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order']

