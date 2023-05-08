from django.contrib import admin
from django.contrib.sites.models import Site

from mptt.admin import DraggableMPTTAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from solo.admin import SingletonModelAdmin

from .forms import CategoryAdminForm
from .models import Category, Header, TopNavigationItem, Product, ProductImage, SiteConfiguration, Footer, \
    FooterColumn1Item, FooterColumn2Item, Popup


admin.site.unregister(Site)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    form = CategoryAdminForm
    search_fields = ('name', 'slug',)
    mptt_level_indent = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'parent', 'home_box_image', 'home_box_text', 'banner')
        }),
        ('Content', {
            'fields': ('content_title_top', 'content_text_top')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

    # Remove Category Submenu Page from footer queryset
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field = form.base_fields['parent']
        field.queryset = field.queryset.filter(level=0)
        return form


@admin.register(Header)
class HeaderAdmin(SingletonModelAdmin):
    pass


@admin.register(TopNavigationItem)
class TopNavigationItemAdmin(DraggableMPTTAdmin):

    def get_list_display(self, request):
        return super().list_display + ('page',)


class ProductImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('__str__', 'is_popular', 'is_on_sale')
    search_fields = ('name', 'slug', 'sku')
    inlines = (ProductImageInline,)
    fieldsets = (
        (None, {
            'fields': (
            'name', 'description', 'sku', 'categories', 'width', 'height', 'depth', 'price_regular', 'price_sale', 'is_popular', 'is_on_sale', 'is_coming_soon')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('google_maps_api_key', 'footer_scripts', 'email_list', 'vanities_link')
        }),
        ('Contact', {
            'fields': (
                'contact_phone', 'contact_address', 'working_hours')
        }),
        ('Disclaimer', {
            'fields': ('disclaimer',)
        }),
        ('Social', {
            'fields': ('facebook_link', 'twitter_link', 'google_plus_link', 'houzz_link')
        }),
    )


class FooterColumn1Inline(SortableInlineAdminMixin, admin.TabularInline):
    model = FooterColumn1Item
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        # Remove Category Submenu Page from footer queryset
        formset = super().get_formset(request, obj, **kwargs)
        field = formset.form.base_fields['page']
        field.queryset = field.queryset.filter(is_category_submenu=False)
        return formset


class FooterColumn2Inline(SortableInlineAdminMixin, admin.TabularInline):
    model = FooterColumn2Item
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        # Remove Category Submenu Page from footer queryset
        formset = super().get_formset(request, obj, **kwargs)
        field = formset.form.base_fields['page']
        field.queryset = field.queryset.filter(is_category_submenu=False)
        return formset


@admin.register(Footer)
class FooterAdmin(SingletonModelAdmin):
    inlines = (FooterColumn1Inline, FooterColumn2Inline)


@admin.register(Popup)
class PopupAdmin(SingletonModelAdmin):

    # Remove Category Submenu Page from footer queryset
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field = form.base_fields['button_page']
        field.queryset = field.queryset.filter(is_category_submenu=False)
        return form
