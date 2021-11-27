import json, random

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None, page=1):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)
    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True,
                quantity__gte=1
            ).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }
        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', context)


def upload(request):
    for product in load_products('./test-data.json'):

        try:
            Product.objects.get(name=product['name'],
                                category_id=int(product['category_id']),
                                price=int(product['price']))
        except ObjectDoesNotExist:
            p = Product.objects.create(name=product['name'],
                                       price=int(product['price']),
                                       category_id=int(product['category_id']),
                                       short_desc=product['short_desc'])
            p.save()

    return render(request, 'mainapp/products.html')


def load_products(file_name) -> list:
    with open(file_name, mode="r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return data['products']


def product(request, pk):
    title = 'Детали'
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': product,
        'same_products': get_same_products(product),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)