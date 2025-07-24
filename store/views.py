from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q

from store.models import Products
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id


def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(
            category=categories, is_available=True)
        paginagtor = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginagtor.get_page(page)
    else:
        products: Products = Products.objects.all().filter(
            is_available=True).order_by("id")
        paginagtor = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginagtor.get_page(page)

    context = {
        "products": page_products,
        "products_count": products.count()
    }

    return render(request, 'App/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Products.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=product)

    except Exception as e:
        raise Http404

    context = {
        "single_product": product,
        "in_cart": in_cart
    }

    return render(request, 'App/product-detail.html', context)


def search(request):
    products = None
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        else:
            products = Products.objects.order_by(
                '-created_date')
    context = {
        "products": products,
        "products_count": products.count()
    }
    return render(request, 'App/store.html', context)
