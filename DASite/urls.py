from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/home.html"), name='home'),
    path('service/seo/', TemplateView.as_view(
        template_name="services/services_seo.html"), name='service_seo'),
    path('service/email/', TemplateView.as_view(
        template_name="services/services_email.html"), name='service_email'),
    path('service/content/', TemplateView.as_view(
        template_name="services/services_content.html"), name='service_content'),
    path('service/smm/', TemplateView.as_view(
        template_name="services/services_smm.html"), name='service_smm'),
    path('service/orm/', TemplateView.as_view(template_name="services/services_orm.html"), name='service_orm'),
    path('service/ppc/', TemplateView.as_view(template_name="services/services_ppc.html"), name='service_ppc'),
    path('admin/', admin.site.urls),
]
