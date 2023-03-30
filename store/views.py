from django.shortcuts import render

from . models import Category, Product
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect 

@csrf_protect 
def store(request):
 
    all_products = Product.objects.all()

    context = {'my_products':all_products}

    return render(request, 'store/store.html', context)

@csrf_protect 
def categories(request):

    all_categories = Category.objects.all()

    return{'all_categories':all_categories}

@csrf_protect 
def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category':category, 'products':products})


@csrf_protect 
def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {'product':product}

    return render(request, 'store/product-info.html', context)