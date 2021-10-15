import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from mainapp.models import ProductCategory, Product


def products(request):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    context = {
        'title': title,
        'links_menu': links_menu,
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
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data['products']
