from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import JsonResponse
from newadmin.models import Product
from user.models import MyUser
from .models import Cart
from django.core import serializers


# Create your views here.


# cart view
def cart_view(request):
    if request.user.is_authenticated:
        cartid = Cart.objects.filter(username = request.user)
        total = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total,"________________")
            # cart = Cart()
            i.sub_total = total
            i.save()
       

        return render(request,'cart.html',{'products': cartid})
    else:
        return render(request,'cart.html')



# add product to cart
@csrf_exempt
def add_cart(request):
    print("buttton clicked")
    if request.method == 'POST':
        id = request.POST['id']
        print('-------',id)
        user = request.user
        product = Product.objects.get(id = id)
        if MyUser.objects.filter(username = user).exists():
            print(' user available',user)
            cart = Cart()
            cart.product_id = product
            cart.username = MyUser.objects.get(username = user) 
            cart.product_stock = 1
            cart.sub_total = product.price
            cart.save()   
        else:
            print('no user___',user)
            request.session['product'] = product.id
            request.session['product_stock'] = 1
            request.session['sub_total'] = product.price
        return JsonResponse({"success":"success"})


# delete prodcut from the cart

def cartitem_dlt(request,id):
    cart_items = Cart.objects.get(id = id)
    cart_items.delete()
    return redirect(cart_view)

@csrf_exempt
def product_increment(request):
    if request.method == 'POST':
        id = request.POST['id']
        cart = Cart.objects.get(product_id = id)
        cart.product_stock += 1
        cart.save()
        cartid = Cart.objects.filter(username = request.user)
        total = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total,"________________")
            # cart = Cart()
            i.sub_total = total
            i.save()
        data = serializers.serialize('json', Cart.objects.filter(product_id = id))

        return JsonResponse({"success": data })
        

@csrf_exempt
def product_decrement(request):
    if request.method == 'POST':
        id = request.POST['id']
        cart = Cart.objects.get(product_id = id)
        cart.product_stock -= 1
        cart.save()
        cartid = Cart.objects.filter(username = request.user)
        total = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total,"________________")
            # cart = Cart()
            i.sub_total = total
            i.save()
        data = serializers.serialize('json', Cart.objects.filter(product_id = id))
        return JsonResponse({"success": data })
    





        

