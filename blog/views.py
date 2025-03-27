from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Post, Category, Tag
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)

        # Фильтрация по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтрация по тегу
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Поиск
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(preview_text__icontains=query) |
                Q(content__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_tags'] = Tag.objects.all()[:10]

        # Получаем параметры фильтрации
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['query'] = self.request.GET.get('q', '')

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем связанные посты
        post = self.get_object()
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            is_published=True
        ).exclude(id=post.id)[:3]

        # Форма комментария
        context['comment_form'] = CommentForm()

        # Комментарии
        context['comments'] = post.comments.filter(is_approved=True)

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,
                             'Ваш комментарий был успешно отправлен и будет опубликован после модерации.')
            return redirect('post_detail', slug=post.slug)

        return self.get(request, *args, **kwargs)