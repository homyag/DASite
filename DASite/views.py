from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import TemplateView
from blog.models import Post
from cases.models import Case
from testimonials.models import Testimonial
from services.models import Service


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


class ServicesListView(TemplateView):
    template_name = 'services/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True).order_by(
            'order')
        return context


class ServiceView(TemplateView):
    def get_template_names(self):
        service_name = self.kwargs.get('service_name')
        return [f"services/services_{service_name}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_name = self.kwargs.get('service_name')

        # Получаем информацию об услуге из базы данных
        service = get_object_or_404(Service, name=service_name, is_active=True)

        # Получаем связанные данные
        features = service.features.all().order_by('order')
        benefits = service.benefits.all().order_by('order')
        processes = service.processes.all().order_by('order')

        # Получаем кейсы, связанные с этой услугой
        related_cases = Case.objects.filter(
            services=service,
            is_published=True
        ).order_by('-created_at')[:3]

        # Добавляем все данные в контекст
        context['service_name'] = service_name
        context['service'] = service
        context['features'] = features
        context['benefits'] = benefits
        context['processes'] = processes
        context['cases'] = related_cases

        # Получаем FAQs для услуги и общие FAQs
        faqs = list(service.faqs.filter(is_common=False).order_by('order'))
        common_faqs = list(
            service.faqs.filter(is_common=True).order_by('order'))
        context['faqs'] = faqs + common_faqs

        return context
