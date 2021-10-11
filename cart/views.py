from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from newadmin.models import Product
from user.models import MyUser
from .models import Cart
from django.http import JsonResponse

# Create your views here.

def cart_view(request):
    product = Cart.objects.filter(username = request.user)
    print(product)
    return render(request,'cart.html',{'products': product})


@csrf_exempt
def add_cart(request):
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

def cartitem_dlt(request,id):
    cart_items = Cart.objects.get(id = id)
    cart_items.delete()
    return redirect(cart_view)



        

