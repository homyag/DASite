from django.contrib import admin
from .models import (
    Service, ServiceFeature, ServiceBenefit, ServiceProcess, FAQ,
    ServiceExplanation, ServiceDetail, ServiceDetailItem,
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


# УДАЛЕН ServiceCaseInline - теперь кейсы управляются через приложение cases


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


class RelatedCasesInline(admin.TabularInline):
    """Inline для отображения связанных кейсов (только для чтения)"""
    from cases.models import Case
    model = Case.services.through
    extra = 0
    readonly_fields = ('case_link',)
    fields = ('case_link',)
    verbose_name = 'Связанный кейс'
    verbose_name_plural = 'Связанные кейсы'

    def case_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        if obj.case:
            url = reverse('admin:cases_case_change', args=[obj.case.pk])
            return format_html('<a href="{}">{}</a>', url, obj.case.title)
        return '-'

    case_link.short_description = 'Кейс'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'slug', 'is_active', 'is_featured', 'order', 'get_cases_count')
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
        ServicePricingInline,
        ServicePartnerInline,
        RelatedCasesInline,  # Заменили ServiceCaseInline на RelatedCasesInline
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

    def get_cases_count(self, obj):
        """Показывает количество связанных кейсов"""
        return obj.get_related_cases().count()

    get_cases_count.short_description = 'Кейсы'


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


# УДАЛЕН ServiceCaseAdmin - кейсы теперь управляются через cases.admin


@admin.register(ServiceExplanation)
class ServiceExplanationAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'description')