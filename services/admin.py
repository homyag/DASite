from django.contrib import admin
from .models import (
    Service, ServiceFeature, ServiceBenefit, ServiceProcess, FAQ,
    ServiceExplanation, ServiceDetail, ServiceDetailItem, ServiceCase,
    ServicePricing, ServicePricingFeature, ServicePartner
)


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


class ServiceExplanationInline(admin.TabularInline):
    model = ServiceExplanation
    extra = 1


class ServiceDetailItemInline(admin.TabularInline):
    model = ServiceDetailItem
    extra = 1


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'description')
    inlines = [ServiceDetailItemInline]


class ServiceDetailInline(admin.TabularInline):
    model = ServiceDetail
    extra = 1
    show_change_link = True


class ServiceCaseInline(admin.TabularInline):
    model = ServiceCase
    extra = 1


class ServicePricingFeatureInline(admin.TabularInline):
    model = ServicePricingFeature
    extra = 1


@admin.register(ServicePricing)
class ServicePricingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'service', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'description')
    inlines = [ServicePricingFeatureInline]


class ServicePricingInline(admin.TabularInline):
    model = ServicePricing
    extra = 1
    show_change_link = True


class ServicePartnerInline(admin.TabularInline):
    model = ServicePartner
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'slug', 'is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ServiceFeatureInline,
        ServiceBenefitInline,
        ServiceProcessInline,
        FAQInline,
        ServiceExplanationInline,
        ServiceDetailInline,
        ServiceCaseInline,
        ServicePricingInline,
        ServicePartnerInline
    ]

    fieldsets = (
        ('Основная информация', {
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
        ('Героическая секция', {
            'fields': ('hero_title', 'hero_description', 'hero_image'),
            'description': 'Настройки верхней части страницы услуги'
        }),
        ('Заголовки секций', {
            'fields': (
                ('explanation_title', 'explanation_subtitle'),
                ('process_title', 'process_subtitle'),
                ('services_title', 'services_subtitle'),
                ('benefits_title', 'benefits_subtitle'),
                ('cases_title', 'cases_subtitle'),
                ('pricing_title', 'pricing_subtitle'),
                ('partners_title', 'partners_subtitle'),
                ('faq_title', 'faq_subtitle'),
                ('contact_title', 'contact_subtitle')
            ),
            'classes': ('collapse',),
            'description': 'Заголовки и подзаголовки для всех секций страницы'
        }),
        ('Контактная информация', {
            'fields': ('contact_phone', 'contact_email'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'service', 'is_common', 'order')
    list_filter = ('service', 'is_common')
    search_fields = ('question', 'answer')


@admin.register(ServicePartner)
class ServicePartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'is_common', 'order')
    list_filter = ('service', 'is_common')
    search_fields = ('name',)


@admin.register(ServiceCase)
class ServiceCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'description')


@admin.register(ServiceExplanation)
class ServiceExplanationAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'description')