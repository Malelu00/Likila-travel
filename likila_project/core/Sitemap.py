from django.contrib.sitemaps import Sitemap
from .models import Event

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'gallery_page']

    def location(self, item):
        from django.urls import reverse
        return reverse(item)

class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Event.objects.filter(status__in=['upcoming', 'active'])

    def lastmod(self, obj):
        return obj.updated_at
