from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin
from solo.admin import SingletonModelAdmin
from jet.admin import CompactInline

from .models import Page, CustomPage, HomePage, HomeBanner, GalleryImage, GalleryPage, OnSalePage, TourPage,\
    ReviewsPage, Review, AboutPage, ContactPage


#admin.site.register(Page, admin.ModelAdmin)


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'content')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


class HomeBannerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = HomeBanner
    extra = 1
    fk_name = 'home_page'

    def get_formset(self, request, obj=None, **kwargs):
        # Disable add/change new pages from inline
        formset = super().get_formset(request, obj, **kwargs)
        widget = formset.form.base_fields['button_page'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


@admin.register(HomePage)
class HomePageAdmin(SingletonModelAdmin):
    inlines = (HomeBannerInline,)
    fieldsets = (
        (None, {
            'fields': ('featured_products',)
        }),
        ('Video Section', {
            'fields': ('video_heading', 'video_description', 'video_embed_url')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


class GalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(GalleryPage)
class GalleryPageAdmin(SingletonModelAdmin):
    inlines = (GalleryImageInline,)
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(OnSalePage)
class OnSalePageAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(TourPage)
class TourPageAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page_title', 'video_tour_url', 'virtual_tour_url')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


class ReviewInline(CompactInline):
    model = Review
    extra = 1


@admin.register(ReviewsPage)
class ReviewsPageAdmin(SingletonModelAdmin):
    inlines = (ReviewInline,)
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text', 'featured_image', 'content')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(ContactPage)
class ContactPageAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('banner', 'banner_text', 'content')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )
