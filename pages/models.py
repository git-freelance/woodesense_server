from django.db import models
from django.urls import reverse

from solo.models import SingletonModel
from redactor.fields import RedactorField

from core.helpers import unique_slugify, upload_common_images_to, upload_gallery_images_to
from core.mixins import SEOModelMixin, BannerModelMixin


class Page(models.Model):
    pid = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    # For using in manually created (Static) pages, e.g HomePage, Contact Page, etc.
    # name = models.CharField(max_length=100, blank=True, null=True)
    # url_name = models.CharField(max_length=200, blank=True, null=True)

    # Normally only one menu item will be category submenu.
    is_category_submenu = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        if self.is_category_submenu:
            return 'Categories Submenu'
        elif hasattr(self, 'homepage'):
            return self.homepage.__str__()
        elif hasattr(self, 'gallerypage'):
            return self.gallerypage.__str__()
        elif hasattr(self, 'onsalepage'):
            return self.onsalepage.__str__()
        elif hasattr(self, 'tourpage'):
            return self.tourpage.__str__()
        elif hasattr(self, 'custompage'):
            return self.custompage.__str__()
        elif hasattr(self, 'reviewspage'):
            return self.reviewspage.__str__()
        elif hasattr(self, 'aboutpage'):
            return self.aboutpage.__str__()
        elif hasattr(self, 'contactpage'):
            return self.contactpage.__str__()
        else:
            return '<Page %s>' % self.pid

    def get_absolute_url(self):
        if self.is_category_submenu:
            return '#'
        elif hasattr(self, 'homepage'):
            return self.homepage.get_absolute_url()
        elif hasattr(self, 'gallerypage'):
            return self.gallerypage.get_absolute_url()
        elif hasattr(self, 'onsalepage'):
            return self.onsalepage.get_absolute_url()
        elif hasattr(self, 'tourpage'):
            return self.tourpage.get_absolute_url()
        elif hasattr(self, 'custompage'):
            return self.custompage.get_absolute_url()
        elif hasattr(self, 'reviewspage'):
            return self.reviewspage.get_absolute_url()
        elif hasattr(self, 'aboutpage'):
            return self.aboutpage.get_absolute_url()
        elif hasattr(self, 'contactpage'):
            return self.contactpage.get_absolute_url()
        else:
            return '#'


###########################
###########################
###########################


class CustomPage(Page, SEOModelMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    banner = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)
    content = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('custom_page', args=[self.slug])

    class Meta:
        verbose_name = 'Custom Page'
        verbose_name_plural = 'Custom Pages'


###########################
###########################
###########################


class HomePage(Page, SEOModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    featured_products = models.ManyToManyField('core.Product', blank=True)

    video_heading = models.CharField(max_length=200, blank=True)
    video_description = models.TextField(blank=True)
    video_embed_url = models.URLField(blank=True)

    def __str__(self):
        return 'Home Page'

    class Meta:
        verbose_name = 'Home Page'

    def get_absolute_url(self):
        return reverse('index')


class HomeBanner(models.Model):
    image = models.ImageField(upload_to=upload_common_images_to)
    header = models.CharField(max_length=100, blank=True, null=True)
    subheader = models.CharField(max_length=200, blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_page = models.ForeignKey('pages.Page', blank=True, null=True, on_delete=models.SET_NULL)
    button_url = models.CharField(max_length=300, blank=True, verbose_name='Or URL')
    home_page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name='banners')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        if self.button_page:
            return self.button_page.get_absolute_url()
        if self.button_url:
            return self.button_url
        return '#'

###########################
###########################
###########################


class GalleryPage(Page, SEOModelMixin, BannerModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    def __str__(self):
        return 'Gallery Page'

    class Meta:
        verbose_name = 'Gallery Page'

    def get_absolute_url(self):
        return reverse('gallery')


class GalleryImage(models.Model):
    gallery_page = models.ForeignKey(GalleryPage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_gallery_images_to)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)


###########################
###########################
###########################


class OnSalePage(Page, SEOModelMixin, BannerModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    def __str__(self):
        return 'On Sale Page'

    class Meta:
        verbose_name = 'On Sale Page'

    def get_absolute_url(self):
        return reverse('on_sale')


###########################
###########################
###########################


class TourPage(Page, SEOModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    page_title = models.CharField(max_length=100, default='TOUR OUR STORE')
    video_tour_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True)

    def __str__(self):
        return 'Tour Page'

    class Meta:
        verbose_name = 'Tour Page'

    def get_absolute_url(self):
        return reverse('tour')


###########################
###########################
###########################


class ReviewsPage(Page, SEOModelMixin, BannerModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model

    def __str__(self):
        return 'Reviews Page'

    class Meta:
        verbose_name = 'Reviews Page'

    def get_absolute_url(self):
        return reverse('reviews')


class Review(models.Model):
    review_page = models.ForeignKey(ReviewsPage, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.text[:15] + '...'

    def get_short_text(self):
        CHARS = 200
        return self.text[:CHARS] + ('...' if len(self.text) > CHARS else '')

###########################
###########################
###########################


class AboutPage(Page, SEOModelMixin, BannerModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    featured_image = models.ImageField(blank=True, null=True, upload_to=upload_common_images_to)
    content = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    def __str__(self):
        return 'About Page'

    class Meta:
        verbose_name = 'About Page'

    def get_absolute_url(self):
        return reverse('about')


class ContactPage(Page, SEOModelMixin, BannerModelMixin, SingletonModel):
    id = models.AutoField(primary_key=True)  # Hack for using inheritance with singleton model
    content = RedactorField(allow_image_upload=True, allow_file_upload=False, blank=True)

    def __str__(self):
        return 'Contact Page'

    class Meta:
        verbose_name = 'Contact Page'

    def get_absolute_url(self):
        return reverse('contact')
