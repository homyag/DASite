from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


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


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    preview_text = models.TextField(verbose_name="Краткое описание")
    content = RichTextUploadingField(verbose_name="Содержание")
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата обновления")
    is_published = models.BooleanField(default=False,
                                       verbose_name="Опубликовано")
    featured_image = models.ImageField(upload_to='blog/',
                                       verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='core_posts',
                                 verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='core_posts', blank=True,
                                  verbose_name="Теги")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='core_posts', verbose_name="Автор")
    meta_title = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name="SEO заголовок")
    meta_description = models.TextField(blank=True, null=True,
                                        verbose_name="SEO описание")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    short_description = models.TextField(verbose_name="Краткое описание")
    client = models.CharField(max_length=100, verbose_name="Клиент")
    content = RichTextUploadingField(verbose_name="Содержание")
    result = models.TextField(verbose_name="Результат")
    featured_image = models.ImageField(upload_to='cases/',
                                       verbose_name="Главное изображение")
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name="Дата создания")
    is_published = models.BooleanField(default=False,
                                       verbose_name="Опубликовано")
    categories = models.ManyToManyField(Category, related_name='cases',
                                        verbose_name="Категории")
    meta_title = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name="SEO заголовок")
    meta_description = models.TextField(blank=True, null=True,
                                        verbose_name="SEO описание")

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('case_detail', kwargs={'slug': self.slug})


class CaseImage(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             related_name='images')
    image = models.ImageField(upload_to='cases/gallery/',
                              verbose_name="Изображение")
    title = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name="Заголовок")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Изображение кейса"
        verbose_name_plural = "Изображения кейсов"
        ordering = ['order']

    def __str__(self):
        return f"Изображение {self.id} для {self.case.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    position = models.CharField(max_length=100, verbose_name="Должность")
    company = models.CharField(max_length=100, verbose_name="Компания")
    content = models.TextField(verbose_name="Содержание отзыва")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True,
                              verbose_name="Фото")
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['order']

    def __str__(self):
        return f"Отзыв от {self.name}, {self.company}"


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