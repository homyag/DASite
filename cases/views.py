from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from core.models import Case, Category


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

        # Поиск
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Получаем параметры фильтрации
        context['current_category'] = self.request.GET.get('category', '')
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
        context['related_cases'] = Case.objects.filter(
            categories__in=case.categories.all(),
            is_published=True
        ).exclude(id=case.id).distinct()[:3]

        return context