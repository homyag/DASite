from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Case, CaseImage
from core.models import Category


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 1
    fields = ('image', 'title', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100" />')
        return '-'

    image_preview.short_description = 'Предпросмотр'


class CaseAdminForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        widgets = {
            'meta_title': forms.TextInput(attrs={'size': 80}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    inlines = [CaseImageInline]
    list_display = ('title', 'client', 'is_published', 'is_featured', 'created_at')
    list_filter = ('is_published', 'is_featured', 'categories')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'short_description', 'content', 'client')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'short_description', 'client', 'content',
                'result', 'featured_image'
            )
        }),
        ('Категоризация', {
            'fields': ('categories',)
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'is_featured', 'created_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
