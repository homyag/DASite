from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Case
from core.models import Category
from services.models import Service


class CaseListView(ListView):
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'cases'
    paginate_by = 9

    def get_queryset(self):
        queryset = Case.objects.filter(is_published=True)

        # Фильтрация по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # НОВЫЙ ФИЛЬТР: Фильтрация по услуге
        service_slug = self.request.GET.get('service')
        if service_slug:
            queryset = queryset.filter(services__slug=service_slug)

        # Поиск
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['services'] = Service.objects.filter(is_active=True)  # НОВОЕ: Добавляем список услуг

        # Получаем параметры фильтрации
        context['current_category'] = self.request.GET.get('category', '')
        context['current_service'] = self.request.GET.get('service', '')  # НОВОЕ: Текущая выбранная услуга
        context['query'] = self.request.GET.get('q', '')

        return context


class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_queryset(self):
        return Case.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем связанные кейсы
        case = self.get_object()

        # УЛУЧШЕННЫЙ АЛГОРИТМ: Ищем похожие кейсы по категориям И услугам
        related_cases = Case.objects.filter(
            Q(categories__in=case.categories.all()) |
            Q(services__in=case.services.all()),
            is_published=True
        ).exclude(id=case.id).distinct()[:3]

        context['related_cases'] = related_cases

        return context


# Дополнительное представление для отображения избранных кейсов на главной
class FeaturedCaseListView(ListView):
    model = Case
    template_name = 'cases/featured_cases.html'
    context_object_name = 'featured_cases'

    def get_queryset(self):
        return Case.objects.filter(is_published=True, is_featured=True).order_by('-created_at')[:6]