from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def main(request):
    title = 'Магазин'

    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'Контакты'
    context = {
        'title': title,
    }
    return render(request, 'geekshop/contact.html', context)
