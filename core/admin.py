from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Expertise


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


# Перерегистрация модели User с нашей кастомной версией
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
