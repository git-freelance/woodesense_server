from urllib.parse import quote_plus

from django import template

from core.models import Category, TopNavigationItem

register = template.Library()


@register.filter
def quoteplus(string):
    string = string.replace('\r', '').replace('\n', '')
    return quote_plus(string, encoding='utf-8')


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ For using paginator with the rest GET params """
    query = context['request'].GET.copy()
    page = kwargs.pop('page')
    query.update(kwargs)
    if page:
        query.__setitem__('page', page)

    return query.urlencode()


@register.simple_tag
def get_root_categories():
    return Category.objects.root_nodes().select_related('parent')


@register.inclusion_tag('core/partials/categories_submenu_desktop.html')
def get_categories_submenu_desktop(root_categories):
    return {'root_categories': root_categories}


@register.inclusion_tag('core/partials/top_menu.html', takes_context=True)
def get_top_menu(context):
    return {'root_items': TopNavigationItem.objects.root_nodes().select_related('page'),
            'categories': Category.objects.all(),
            'site_config': context['site_config']}


@register.inclusion_tag('core/partials/product_box.html')
def get_product_box(product, show_featured_label=False, show_prices=False):
    return {'product': product, 'show_featured_label': show_featured_label, 'show_prices': show_prices}


@register.inclusion_tag('core/partials/review_box.html')
def get_review_box(review, full_text=0):
    return {'review': review, 'full_text': full_text}
