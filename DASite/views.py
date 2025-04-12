from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from blog.models import Post
from cases.models import Case
from testimonials.models import Testimonial
from services.models import (
    Service, ServiceFeature, ServiceBenefit, ServiceProcess, FAQ,
    ServiceExplanation, ServiceDetail, ServiceCase, ServicePricing, ServicePartner
)


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем избранные отзывы для главной страницы
        context['testimonials'] = Testimonial.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('order')[:6]  # Ограничиваем количество отзывов

        # Получаем избранные кейсы
        context['featured_cases'] = Case.objects.filter(
            is_published=True,
            is_featured=True
        ).prefetch_related('categories').order_by('-created_at')[:6]

        # Получаем последние статьи блога для главной
        context['featured_posts'] = Post.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-created_at')[:3]

        # Получаем все услуги для отображения в секции услуг
        context['services'] = Service.objects.filter(
            is_active=True,
            is_featured=True
        ).prefetch_related('features').order_by('order')

        return context