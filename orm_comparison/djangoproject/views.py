from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import get_object_or_404


def product_list(request):
    products = Product.objects.all()
    return render(request, 'djangoproject/product_list.html', {'products': products})


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
