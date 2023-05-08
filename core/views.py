import json

from django.core import paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView

from pages.models import CustomPage, HomePage, GalleryPage, GalleryImage, OnSalePage, TourPage, ReviewsPage, Review, \
    AboutPage, ContactPage
from .forms import ContactForm
from .models import Category, Product


class IndexView(TemplateView):
    template_name = 'core/pages/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        home_page_solo = HomePage.get_solo()
        tour_page_solo = TourPage.get_solo()
        ctx['solo'] = home_page_solo
        ctx['reviews'] = Review.objects.all()
        ctx['contact_form'] = ContactForm()
        ctx['images_json'] = json.dumps({'images': [x.image.url for x in GalleryImage.objects.all()]})
        ctx['video_tour_url'] = tour_page_solo.video_tour_url
        ctx['virtual_tour_url'] = tour_page_solo.virtual_tour_url
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/pages/product_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.object = self.get_object()
        MAX_RELATED_PRODUCTS = 4
        subcategory = self.object.categories.filter(level=1)
        if subcategory.exists():
            # Get related products from subcategory
            category = subcategory.first()
            related_products = category.products.all().exclude(id=self.object.id)[:MAX_RELATED_PRODUCTS]
            ctx['related_products'] = related_products
        return ctx


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'core/pages/category_detail.html'
    paginate_products_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.category_popular_slug = kwargs.get('category_popular')
        self.category_path = kwargs.get('path')
        self.page = request.GET.get('page')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.category_popular_slug:
            return get_object_or_404(self.model, slug=self.category_popular_slug)  # TODO select related
        elif self.category_path:
            last_slug = self.category_path.split('/')[-1]
            return get_object_or_404(self.model, slug=last_slug)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['reviews'] = Review.objects.all().order_by('?')[:2]
        products = self.get_object().products.all()

        if self.category_popular_slug:
            ctx['is_popular'] = True
            products = products.filter(is_popular=True)

        products_paginator = paginator.Paginator(products, self.paginate_products_by)
        try:
            products_page_obj = products_paginator.page(self.page)
        except (paginator.PageNotAnInteger, paginator.EmptyPage):
            products_page_obj = products_paginator.page(1)

        ctx['products'] = products_page_obj
        return ctx


class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'core/pages/gallery_list.html'
    # paginate_by = 20
    context_object_name = 'images'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['solo'] = GalleryPage.get_solo()
        return ctx


class OnSaleListView(ListView):
    model = Product
    template_name = 'core/pages/on_sale_list.html'
    paginate_by = 16
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(is_on_sale=True)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['solo'] = OnSalePage.get_solo()
        return ctx


class TourDetailView(DetailView):
    model = TourPage
    template_name = 'core/pages/tour_detail.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()


class SearchListView(ListView):
    model = Product
    template_name = 'core/pages/search_list.html'
    paginate_by = 16
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            q = q.strip()
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(sku__icontains=q))
            return qs
        else:
            raise Http404


class CustomPageDetailView(DetailView):
    model = CustomPage
    template_name = 'core/pages/custom_page_detail.html'
    context_object_name = 'page'


class ReviewsListView(ListView):
    model = Review
    template_name = 'core/pages/reviews_list.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['solo'] = ReviewsPage.get_solo()
        return ctx


class AboutDetailView(DetailView):
    model = AboutPage
    template_name = 'core/pages/about_detail.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['images_json'] = json.dumps({'images': [x.image.url for x in GalleryImage.objects.all()]})
        return ctx


class ContactDetailView(FormView):
    form_class = ContactForm
    template_name = 'core/pages/contact_detail.html'
    success_url = reverse_lazy('custom_page', kwargs={'slug': 'thank-you'})

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = ContactPage.get_solo()
        return ctx
