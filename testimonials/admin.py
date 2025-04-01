from django.contrib import admin
from django.utils.html import format_html
from testimonials.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'position', 'rating_display', 'is_published', 'is_featured', 'order')
    list_filter = ('is_published', 'is_featured', 'rating')
    list_editable = ('is_published', 'is_featured', 'order')
    search_fields = ('name', 'company', 'content', 'position')

    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FFD700;">{}</span>', stars)

    rating_display.short_description = 'Рейтинг'