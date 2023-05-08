from django.contrib.sitemaps import Sitemap
from .models import Category, Product
from pages.models import Page

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url

    # def lastmod(self, obj):
    #     return obj.pub_date


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_date


class PageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Page.objects.all()

