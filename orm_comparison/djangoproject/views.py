from django.shortcuts import render, redirect
from .models import Product
from django.db.models import Avg
from django.shortcuts import get_object_or_404


def product_list(request):
    # Все товары
    products = Product.objects.all()

    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Фильтр по количеству на складе
    sort_by_stock = request.GET.get('sort')
    if sort_by_stock == 'stock':
        products = products.order_by('stock')

    # Фильтр по описанию
    description_filter = request.GET.get('description')
    if description_filter:
        products = products.filter(description__icontains=description_filter)

    # Средняя цена
    average_price = products.aggregate(Avg('price'))['price__avg']

    return render(request, 'djangoproject/product_list.html', {
        'products': products,
        'average_price': average_price,
    })


def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        description = request.POST['description']
        Product.objects.create(name=name, price=price, stock=stock, description=description)
        return redirect('product_list')
    return render(request, 'djangoproject/product_create.html')


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.description = request.POST['description']
        product.save()
        return redirect('product_list')
    return render(request, 'djangoproject/product_update.html', {'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'djangoproject/product_delete.html', {'product': product})
