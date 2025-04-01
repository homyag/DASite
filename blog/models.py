# blog/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Category, Tag


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
                                 related_name='blog_posts',
                                 verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True,
                                  verbose_name="Теги")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='blog_posts', verbose_name="Автор")
    meta_title = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name="SEO заголовок")
    meta_description = models.TextField(blank=True, null=True,
                                        verbose_name="SEO описание")
    is_featured = models.BooleanField(default=False,
                                      verbose_name="Отображать на главной")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name="Статья")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрен")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.name} к {self.post.title}"
