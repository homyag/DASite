from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Comment
from core.models import Category, Tag
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4

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
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('blog_posts')
        ).order_by('-post_count')[:10]

        # Получаем параметры фильтрации
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['query'] = self.request.GET.get('q', '')

        # Добавляем название текущей категории (для отображения в breadcrumbs)
        if context['current_category']:
            try:
                category = Category.objects.get(
                    slug=context['current_category'])
                context['current_category_name'] = category.name
            except Category.DoesNotExist:
                context['current_category_name'] = context['current_category']

        # Добавляем название текущего тега (для отображения в breadcrumbs)
        if context['current_tag']:
            try:
                tag = Tag.objects.get(slug=context['current_tag'])
                context['current_tag_name'] = tag.name
            except Tag.DoesNotExist:
                context['current_tag_name'] = context['current_tag']

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Получаем связанные посты - не более 3 последних постов автора, исключая текущий
        context['author_posts'] = post.author.blog_posts.filter(
            is_published=True
        ).exclude(id=post.id).order_by('-created_at')[:3]

        # Получаем связанные посты по категории - не более 3, исключая текущий
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            is_published=True
        ).exclude(id=post.id).order_by('-created_at')[:3]

        # Получаем связанные посты по тегам - не более 3, исключая текущий и уже включенные посты
        if post.tags.exists():
            excluded_ids = [post.id] + [rp.id for rp in
                                        context['related_posts']]
            tag_related_posts = Post.objects.filter(
                tags__in=post.tags.all(),
                is_published=True
            ).exclude(
                id__in=excluded_ids
            ).distinct().order_by('-created_at')[:3]

            context['tag_related_posts'] = tag_related_posts

        # Форма комментария
        context['comment_form'] = CommentForm()

        # Комментарии
        context['comments'] = post.comments.filter(is_approved=True)

        return context


# Дополнительное представление для отображения избранных постов на главной
class FeaturedPostListView(ListView):
    model = Post
    template_name = 'blog/featured_posts.html'
    context_object_name = 'featured_posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True,
                                   is_featured=True).order_by('-created_at')[
               :3]
