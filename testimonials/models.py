# testimonials/models.py
from django.db import models


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
    is_featured = models.BooleanField(default=False,
                                      verbose_name="Отображать на главной")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['order']

    def __str__(self):
        return f"Отзыв от {self.name}, {self.company}"
