# services/models.py
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    """Модель для хранения информации об услугах агентства"""
    name = models.CharField('Название услуги', max_length=100)
    slug = models.SlugField('URL-идентификатор', max_length=100, unique=True)
    title = models.CharField('Заголовок страницы', max_length=200)
    description = models.TextField('Краткое описание', max_length=500)
    full_description = models.TextField('Полное описание')

    icon_svg = models.TextField('SVG-иконка', blank=True, help_text="Вставьте SVG-код иконки")
    icon = models.CharField('Иконка (класс или SVG)', max_length=500, blank=True)
    image = models.ImageField('Изображение услуги', upload_to='services/', blank=True)

    is_active = models.BooleanField('Активно', default=True)
    is_featured = models.BooleanField('Отображать на главной', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    meta_title = models.CharField('Meta Title', max_length=200, blank=True)
    meta_description = models.TextField('Meta Description', max_length=500, blank=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    hero_title = models.CharField('Заголовок героической секции', max_length=200, blank=True)
    hero_description = models.TextField('Описание героической секции', blank=True)
    hero_image = models.ImageField('Изображение героической секции', upload_to='services/hero/', blank=True)

    explanation_title = models.CharField('Заголовок секции "Что такое"', max_length=200, blank=True)
    explanation_subtitle = models.TextField('Подзаголовок секции "Что такое"', blank=True)

    process_title = models.CharField('Заголовок секции "Как мы работаем"', max_length=200, blank=True)
    process_subtitle = models.TextField('Подзаголовок секции "Как мы работаем"', blank=True)

    services_title = models.CharField('Заголовок секции "Наши услуги"', max_length=200, blank=True)
    services_subtitle = models.TextField('Подзаголовок секции "Наши услуги"', blank=True)

    benefits_title = models.CharField('Заголовок секции "Преимущества"', max_length=200, blank=True)
    benefits_subtitle = models.TextField('Подзаголовок секции "Преимущества"', blank=True)

    cases_title = models.CharField('Заголовок секции "Кейсы"', max_length=200, blank=True)
    cases_subtitle = models.TextField('Подзаголовок секции "Кейсы"', blank=True)

    pricing_title = models.CharField('Заголовок секции "Тарифы"', max_length=200, blank=True)
    pricing_subtitle = models.TextField('Подзаголовок секции "Тарифы"', blank=True)

    partners_title = models.CharField('Заголовок секции "Партнеры"', max_length=200, blank=True)
    partners_subtitle = models.TextField('Подзаголовок секции "Партнеры"', blank=True)

    faq_title = models.CharField('Заголовок секции "FAQ"', max_length=200, blank=True)
    faq_subtitle = models.TextField('Подзаголовок секции "FAQ"', blank=True)

    # Контактная информация
    contact_title = models.CharField('Заголовок секции "Контакты"', max_length=200, blank=True)
    contact_subtitle = models.TextField('Подзаголовок секции "Контакты"', blank=True)
    contact_phone = models.CharField('Телефон для связи', max_length=100, blank=True)
    contact_email = models.EmailField('Email для связи', blank=True)

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


# Оставляем существующие модели без изменений
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
    answer = models.TextField('Ответ')
    is_common = models.BooleanField('Общий вопрос', default=False,
                                    help_text='Отметьте, если вопрос относится ко всем услугам')
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order']


# Добавляем новые модели для поддержки всех секций страницы
class ServiceExplanation(models.Model):
    """Модель для блоков с объяснением (Что такое SEO, преимущества и т.д.)"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='explanations')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    icon_svg = models.TextField('SVG-иконка', blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Блок объяснения'
        verbose_name_plural = 'Блоки объяснений'
        ordering = ['order']


class ServiceDetail(models.Model):
    """Модель для детального описания услуг (блоки с услугами на странице)"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='details')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    icon_svg = models.TextField('SVG-иконка', blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Детальная услуга'
        verbose_name_plural = 'Детальные услуги'
        ordering = ['order']


class ServiceDetailItem(models.Model):
    """Пункты для детальных услуг"""
    detail = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE, related_name='items')
    text = models.CharField('Текст пункта', max_length=200)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.text} ({self.detail.title})"

    class Meta:
        verbose_name = 'Пункт детальной услуги'
        verbose_name_plural = 'Пункты детальных услуг'
        ordering = ['order']


class ServiceCase(models.Model):
    """Кейсы услуг"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='services/cases/')
    category = models.CharField('Категория', max_length=100)
    result = models.CharField('Результат', max_length=100)
    link = models.URLField('Ссылка на подробности', blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'
        ordering = ['order']


class ServicePricing(models.Model):
    """Тарифы услуг"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='pricing')
    title = models.CharField('Название тарифа', max_length=100)
    price = models.CharField('Цена', max_length=100)
    period = models.CharField('Период', max_length=50, default='в месяц')
    description = models.CharField('Краткое описание', max_length=200, blank=True)
    badge = models.CharField('Бейдж (например, Рекомендуемый)', max_length=100, blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.title} ({self.service.name})"

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['order']


class ServicePricingFeature(models.Model):
    """Функции тарифов"""
    pricing = models.ForeignKey(ServicePricing, on_delete=models.CASCADE, related_name='features')
    text = models.CharField('Текст функции', max_length=200)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return f"{self.text} ({self.pricing.title})"

    class Meta:
        verbose_name = 'Функция тарифа'
        verbose_name_plural = 'Функции тарифов'
        ordering = ['order']


class ServicePartner(models.Model):
    """Партнеры и инструменты"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='partners', null=True, blank=True)
    name = models.CharField('Название', max_length=100)
    logo = models.ImageField('Логотип', upload_to='services/partners/')
    link = models.URLField('Ссылка', blank=True)
    is_common = models.BooleanField('Общий партнер', default=False)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['order']