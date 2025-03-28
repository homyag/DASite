from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Service(models.Model):
    """Модель для хранения информации об услугах агентства"""
    name = models.CharField('Название услуги', max_length=100)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)
    title = models.CharField('Заголовок страницы', max_length=200)
    description = models.TextField('Краткое описание', max_length=500)
    full_description = RichTextField('Полное описание')
    icon = models.CharField('Иконка (класс или SVG)', max_length=500,
                            blank=True)
    image = models.ImageField('Изображение услуги', upload_to='services/',
                              blank=True)
    is_active = models.BooleanField('Активно', default=True)
    meta_title = models.CharField('Meta Title', max_length=200, blank=True)
    meta_description = models.TextField('Meta Description', max_length=500,
                                        blank=True)
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
    answer = RichTextField('Ответ')
    is_common = models.BooleanField('Общий вопрос', default=False,
                                    help_text='Отметьте, если вопрос относится ко всем услугам')
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order']


class Case(models.Model):
    """Модель для хранения кейсов (портфолио)"""
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)
    services = models.ManyToManyField(Service, related_name='cases',
                                      verbose_name='Связанные услуги')
    description = models.TextField('Краткое описание', max_length=500)
    full_description = RichTextField('Полное описание')
    image = models.ImageField('Изображение кейса', upload_to='cases/')
    result = models.CharField('Результат', max_length=200, blank=True)
    client = models.CharField('Клиент', max_length=200, blank=True)
    is_featured = models.BooleanField('Размещать на главной', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'
        ordering = ['-created_at']
