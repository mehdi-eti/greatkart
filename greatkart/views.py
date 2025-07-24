from django.shortcuts import render

from store.models import Products


def index(request):
    products = Products.objects.all().filter(is_available=True)
    context = {
        "products": products,
    }
    return render(request, 'App/index.html', context)
