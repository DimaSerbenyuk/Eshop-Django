from django.shortcuts import render

from .cart import Cart #need to check our session

from store.models import Product

from django.views.decorators.csrf import csrf_protect 

from django.shortcuts import get_object_or_404

from django.http import JsonResponse


@csrf_protect 
def cart_summory(request): # obtain session data and pass it on through out cart-summory.html(page)

    cart = Cart(request)
    
    return render(request, 'cart-summary.html', {'cart':cart})

@csrf_protect 
def cart_add(request):

    cart = Cart(request) #we are making use of session class cart()

    if request.POST.get('action') == 'post': 

        product_id = int(request.POST.get('product_id'))

        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_qty=product_quantity)
        
        cart_quantity = cart.__len__()
        
        response = JsonResponse({'qty': cart_quantity})

        return response

@csrf_protect 
def cart_delete(request):

    cart = Cart(request) #we are making use of session class cart()

    if request.POST.get('action') == 'post': 

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id) #info pr_id from Ajax (cart-sum.html)

        cart_quantity = cart.__len__() #update qty val 

        cart_total = cart.get_total() #update total price


        
        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response
        
        

@csrf_protect 
def cart_update(request):
    
    cart = Cart(request)

    if request.POST.get('action') == 'post': 

        product_id = int(request.POST.get('product_id'))

        product_quantity = int(request.POST.get('product_quantity')) # <--- HERE ERROR

        cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response