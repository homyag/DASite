from django.contrib import admin
from django import forms
from blog.models import Post, Comment
from core.models import Category, Tag


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'meta_title': forms.TextInput(attrs={'size': 80}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'is_published', 'is_featured', 'created_at')
    list_filter = ('is_published', 'is_featured', 'category', 'tags')
    search_fields = ('title', 'preview_text', 'content')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'tags', 'author']
    list_editable = ('is_published', 'is_featured')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'preview_text', 'content', 'featured_image',
                'author'
            )
        }),
        ('Категоризация', {
            'fields': ('category', 'tags')
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'is_featured', 'created_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"


# Настраиваем автозаполнение для категорий и тегов
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}