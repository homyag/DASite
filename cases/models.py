# cases/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse

from tinymce.models import HTMLField

from core.models import Category
from services.models import Service


class Case(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    short_description = models.TextField(verbose_name="Краткое описание")
    client = models.CharField(max_length=100, verbose_name="Клиент")
    content = HTMLField(verbose_name="Содержание")
    result = models.TextField(verbose_name="Результат")
    featured_image = models.ImageField(upload_to='cases/',
                                       verbose_name="Главное изображение")
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name="Дата создания")
    is_published = models.BooleanField(default=False,
                                       verbose_name="Опубликовано")
    categories = models.ManyToManyField(Category, related_name='cases',
                                        verbose_name="Категории")
    services = models.ManyToManyField(Service, related_name='case_services',
                                      verbose_name="Связанные услуги",
                                      blank=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name="SEO заголовок")
    meta_description = models.TextField(blank=True, null=True,
                                        verbose_name="SEO описание")
    is_featured = models.BooleanField(default=False,
                                      verbose_name="Отображать на главной")

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
