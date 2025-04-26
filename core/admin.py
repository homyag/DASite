from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Expertise, Newsletter, ContactRequest


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'
    fields = (
        ('photo',),
        ('bio',),
        ('position', 'company'),
        ('linkedin_url', 'twitter_url'),
        ('github_url', 'website_url'),
        ('expertise', 'years_experience'),
    )
    filter_horizontal = ('expertise',)


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'get_position')
    list_select_related = ('profile',)

    def get_position(self, instance):
        return instance.profile.position if hasattr(instance,
                                                    'profile') else ''

    get_position.short_description = 'Должность'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'
    actions = ['deactivate_subscribers', 'activate_subscribers']

    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} подписчиков деактивировано.")
    deactivate_subscribers.short_description = "Деактивировать выбранных подписчиков"

    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} подписчиков активировано.")
    activate_subscribers.short_description = "Активировать выбранных подписчиков"


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'email', 'phone', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'service', 'message')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Запрещаем добавление заявок вручную через админку
        return False


# Перерегистрация модели User с нашей кастомной версией
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
