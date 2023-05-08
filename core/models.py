from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.functional import cached_property
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from solo.models import SingletonModel
from colorful.fields import RGBColorField

from .mixins import SEOModelMixin
from .helpers import unique_slugify, upload_common_images_to, upload_product_images_to, upload_gallery_images_to


class Category(MPTTModel, SEOModelMixin):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)

    home_box_image = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)
    home_box_text = models.CharField(max_length=200, blank=True)
    banner = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)

    content_title_top = models.CharField(max_length=200, blank=True, verbose_name='Title Top')
    content_text_top = models.TextField(blank=True, verbose_name='Text Top')

    # content_title_bottom = models.CharField(max_length=200, blank=True, verbose_name='Title Bottom')
    # content_text_bottom = models.TextField(blank=True, verbose_name='Text Bottom')

    # order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    @cached_property
    def get_absolute_url(self):
        path = '/'.join([x.slug for x in self.get_ancestors(include_self=True)])
        return reverse('category', args=[path])

    class Meta:
        # ordering = ('order',)
        verbose_name_plural = 'Categories'
        unique_together = (('name', 'parent',),)

    def get_banner_image(self):
        if self.banner:
            return self.banner.url

        if not self.is_root_node():
            return self.get_root().get_banner_image()

        return ''


# NAVI


class Header(SingletonModel):
    header_color_sides = RGBColorField(default='#01123e')
    header_color_center = RGBColorField(default='#306da3')

    def __str__(self):
        return 'Header'

    class Meta:
        verbose_name = 'Header'


class TopNavigationItem(MPTTModel):
    name = models.CharField(max_length=50, unique=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.SET_NULL)
    page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=300, blank=True, verbose_name='Or URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.page_id is not None:
            return self.page.get_absolute_url()
        elif self.url:
            return self.url
        else:
            return '#'

    class Meta:
        verbose_name = 'Navigation Item'
        unique_together = (('name', 'parent',),)


class Product(SEOModelMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    description = models.TextField(blank=True)
    sku = models.CharField(max_length=70, blank=True, verbose_name='SKU')
    categories = TreeManyToManyField(Category, related_name='products')

    price_regular = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Regular price')
    price_sale = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Sale price')

    is_popular = models.BooleanField(default=False, verbose_name='Popular')
    is_on_sale = models.BooleanField(default=False, verbose_name='On sale')
    is_coming_soon = models.BooleanField(default=False, verbose_name='Coming soon')

    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    depth = models.FloatField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_featured_image(self):
        if self.images.exists():
            return self.images.first()
        return None

    def get_breadcrumb(self):
        return self.categories.all().order_by('level')

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    class Meta:
        ordering = ('-is_popular', '-created_date',)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_product_images_to)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)


class SiteConfiguration(SingletonModel):
    google_maps_api_key = models.CharField(blank=True, max_length=200)
    footer_scripts = models.TextField(blank=True, help_text="Don't forget to wrap code in &lt;script&gt; tag")
    email_list = models.TextField(blank=True, help_text="One email per line")
    vanities_link = models.URLField(blank=True)

    contact_phone = models.CharField(max_length=100, blank=True)
    contact_address = models.TextField(blank=True)
    # contact_email = models.EmailField(blank=True)
    working_hours = models.TextField(blank=True)

    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    google_plus_link = models.URLField(blank=True)
    houzz_link = models.URLField(blank=True)

    disclaimer = models.TextField(blank=True)

    def __str__(self):
        return 'Site Configuration'

    class Meta:
        verbose_name = 'Site Configuration'


############################
############################


class Footer(SingletonModel):
    copyright_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return 'Footer'

    class Meta:
        verbose_name = 'Footer'


class AbstractFooterColumnItem(models.Model):
    name = models.CharField(max_length=50)
    page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=300, blank=True, verbose_name='Or URL')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('order',)

    def get_absolute_url(self):
        if self.page_id is not None:
            return self.page.get_absolute_url()
        elif self.url:
            return self.url
        else:
            return '#'


class FooterColumn1Item(AbstractFooterColumnItem):

    class Meta(AbstractFooterColumnItem.Meta):
        verbose_name = 'Footer Column 1 Item'
        verbose_name_plural = 'Footer Column 1 Items'


class FooterColumn2Item(AbstractFooterColumnItem):

    class Meta(AbstractFooterColumnItem.Meta):
        verbose_name = 'Footer Column 2 Item'
        verbose_name_plural = 'Footer Column 2 Items'


###############


class Popup(SingletonModel):
    enabled = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)
    button_text = models.CharField(max_length=50, blank=True)
    button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL)
    button_url = models.CharField(max_length=300, blank=True, verbose_name='Or URL')
    delay = models.IntegerField(default=3, help_text='In seconds')

    def __str__(self):
        return 'Popup'

    class Meta:
        verbose_name = 'Popup'

    def get_absolute_url(self):
        if self.button_page_id is not None:
            return self.button_page.get_absolute_url()
        elif self.button_url:
            return self.button_url
        else:
            return '#'


