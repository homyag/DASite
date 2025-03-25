from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from DASite.views import ServiceView


urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/home.html"),
         name='home'),

    # Новый паттерн
    path('service/<str:service_name>/', ServiceView.as_view(), name='service'),

    # Fixed individual service URLs
    path('service/seo/', ServiceView.as_view(), {'service_name': 'seo'},
         name='service_seo'),
    path('service/email/', ServiceView.as_view(), {'service_name': 'email'},
         name='service_email'),
    path('service/content/', ServiceView.as_view(),
         {'service_name': 'content'}, name='service_content'),
    path('service/smm/', ServiceView.as_view(), {'service_name': 'smm'},
         name='service_smm'),
    path('service/orm/', ServiceView.as_view(), {'service_name': 'orm'},
         name='service_orm'),
    path('service/ppc/', ServiceView.as_view(), {'service_name': 'ppc'},
         name='service_ppc'),

    path('admin/', admin.site.urls),
]