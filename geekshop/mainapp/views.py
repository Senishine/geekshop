import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def products(request, pk=None):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    products = Product.objects.all().order_by('price')

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
        }

        return render(request, 'mainapp/products.html', context)

    same_products = Product.objects.all()[1:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'products': products,
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


