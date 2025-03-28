from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from core.models import Case


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'post_list', 'case_list', 'contact']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['service_seo', 'service_email', 'service_content',
                'service_smm', 'service_orm', 'service_ppc']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class CaseSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Case.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at
