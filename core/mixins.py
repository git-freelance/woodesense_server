from django.db import models

from .helpers import upload_common_images_to


class SEOModelMixin(models.Model):
    seo_title = models.CharField(max_length=100, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class BannerModelMixin(models.Model):
    banner = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)
    banner_text = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True
