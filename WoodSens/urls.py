"""WoodSens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from core.views import IndexView, ProductDetailView, CategoryDetailView, GalleryListView, OnSaleListView, \
    TourDetailView, SearchListView, CustomPageDetailView, ReviewsListView, AboutDetailView, ContactDetailView
from core.sitemaps import CategorySitemap, ProductSitemap, PageSitemap


sitemaps = {
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
    path('redactor/', include('redactor.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('', IndexView.as_view(), name='index'),
    path('page/<slug:slug>/', CustomPageDetailView.as_view(), name='custom_page'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('category/<slug:category_popular>/popular/', CategoryDetailView.as_view(), name='category_popular'),
    path('category/<path:path>/', CategoryDetailView.as_view(), name='category'),
    path('gallery/', GalleryListView.as_view(), name='gallery'),
    path('on-sale/', OnSaleListView.as_view(), name='on_sale'),
    path('tour/', TourDetailView.as_view(), name='tour'),
    path('search/', SearchListView.as_view(), name='search'),
    path('reviews/', ReviewsListView.as_view(), name='reviews'),
    path('about/', AboutDetailView.as_view(), name='about'),
    path('contact/', ContactDetailView.as_view(), name='contact'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.TOOLBAR_ENABLED:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
