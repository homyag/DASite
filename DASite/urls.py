from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.sitemaps.views import sitemap


from DASite.views import HomePageView, PrivacyPolicyView, TermsOfUseView
from services.views import ServicesListView, ServiceView
from contacts.views import contact_view, contact_success_view, \
    contact_submit_view
from blog.views import PostListView, PostDetailView
from cases.views import CaseListView, CaseDetailView
from DASite.sitemaps import (StaticViewSitemap, ServiceSitemap, BlogSitemap,
                             CaseSitemap)


sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
    'cases': CaseSitemap,
}


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /ckeditor/",
        "Sitemap: https://{}/sitemap.xml".format(request.get_host()),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('contact/submit/', contact_submit_view, name='contact_submit'),  # Только для обработки POST
    path('contact/success/', contact_success_view, name='contact_success'),

    path('services/', ServicesListView.as_view(), name='services_list'),

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

    path('contacts/', contact_view, name='contact'),
    # path('contacts/success/', contact_success_view, name='contact_success'),
    path('contact/submit/', contact_submit_view, name='contact_submit'),  # Только для обработки POST
    path('contact/success/', contact_success_view, name='contact_success'),

    path('admin/', admin.site.urls),

    # Tynymce
    path('tinymce/', include('tinymce.urls')),

    # Blog URLs
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

    # Cases URLs
    path('cases/', CaseListView.as_view(), name='case_list'),
    path('cases/<slug:slug>/', CaseDetailView.as_view(), name='case_detail'),

    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),

    path('terms-of-use/', TermsOfUseView.as_view(), name='terms_of_use'),

    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)