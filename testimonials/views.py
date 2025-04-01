# testimonials/views.py
from django.views.generic import ListView
from .models import Testimonial


class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'

    def get_queryset(self):
        return Testimonial.objects.filter(is_published=True).order_by('order')


# Представление для отображения избранных отзывов на главной
class FeaturedTestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/featured_testimonials.html'
    context_object_name = 'featured_testimonials'

    def get_queryset(self):
        return Testimonial.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('order')