from django.contrib import admin
from .models import Service, ServiceBenefit, ServiceProcess, FAQ, Case, \
    ServiceFeature


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1


class ServiceProcessInline(admin.TabularInline):
    model = ServiceProcess
    extra = 1


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'slug', 'is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFeatureInline, ServiceBenefitInline, ServiceProcessInline, FAQInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'title', 'description', 'full_description')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Медиа', {
            'fields': ('icon_svg', 'icon', 'image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'service', 'is_common', 'order')
    list_filter = ('service', 'is_common')
    search_fields = ('question', 'answer')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'is_featured')
    list_filter = ('services', 'is_featured')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('services',)