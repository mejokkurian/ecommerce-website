from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from newadmin.views import user_active
from django.http import JsonResponse
from newadmin.models import Product
from newadmin.models import Coupon
from order.models import Address
from user.models import MyUser
from user.views import home
from .models import Cart
import datetime
import uuid

# Create your views here.


# cart view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_view(request):
    if request.user.is_authenticated:
        coupons = Coupon.objects.all()
        cartid = Cart.objects.filter(username=request.user).order_by('id')
        total = 0
        item = 0
        stock = 0
        grand_total = 0
        tax = 0
        for i in cartid:
            if i.product_id.discount_price == None:
                total = i.product_id.price * i.product_stock
                i.sub_total = total
                i.save()
            else:
                total = i.product_id.discount_price * i.product_stock
                i.sub_total = total
                i.save()

            grand_total += total
            tax = (grand_total/100)*5
        return render(request, 'cart.html', {'products': cartid, 'grandtotal': grand_total, 'tax': tax, 'coupons':coupons})
    messages.error(request,"please login!!!")    
    return redirect('login')

# add product to cart
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def add_cart(request): 
    if request.method == 'POST':
        id = request.POST['id']
        user = request.user
        product = Product.objects.get(id=id)

        if request.user.is_authenticated:
            if MyUser.objects.filter(username=user).exists():
                cart = Cart()
                print(cart)
                cart.product_id = product
                cart.username = MyUser.objects.get(username=user)
                newuser = cart.username
                cart.product_stock = 1
                cart.sub_total = product.price

                cartItem = Cart.objects.filter(product_id=id, username = request.user).first()
                print(cartItem)
                if cartItem:
                    print('entered')
                else:
                    cart.save()

                cart_items = Cart.objects.filter(username = request.user).count()
                print(type(cart_items))
                return JsonResponse({'cart_items': cart_items})
        else:
            if request.session.has_key('guest_user'):
                g_cart = Cart()
                g_cart.guest_token = request.session['guest_user']
                g_cart.product_id = product
                g_cart.username = None
                g_cart.product_stock = 1
                g_cart.sub_total = product.price
                v = Cart.objects.filter(product_id=id, guest_token = request.session['guest_user']).first()
                if v:
                    print("product already in cart")
                else:
                    g_cart.save() 

                carteii = Cart.objects.filter(guest_token = request.session['guest_user']).count()
                return JsonResponse({'cart_items': carteii})     
            else:
                guest_user = str(uuid.uuid1())
                print(guest_user)
                request.session['poli'] = True
                request.session['guest_user'] = guest_user
                cart2 = Cart()
                cart2.guest_token = guest_user
                cart2.product_id = product
                cart2.username = None
                cart2.product_stock = 1
                cart2.sub_total = product.price
                b = Cart.objects.filter(product_id=id, guest_token = guest_user).first()
                if b:
                    print("already in the cart")
                else:
                    cart2.save()

                carteee = Cart.objects.filter(guest_token = guest_user).count()
                print(carteee)
                return JsonResponse({'cart_items': carteee})     
                

    else:
        errorr = "error"
        return JsonResponse({'errorr': errorr})



# delete prodcut from the cart
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def cartitem_dlt(request):
    id = request.POST['id']
    cart_items = Cart.objects.get(id=id)
    cart_items.delete()
    success = "done"
    return JsonResponse({"success":success})


# product increment in cart
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_increment(request):
    if request.method == 'POST':
        id = request.POST['id']
        product = Product.objects.get(id=id)
        stock = product.amount_in_stock

        #adding stock to cart
        cart = Cart.objects.get(product_id=id,username = request.user)
        cart.product_stock += 1
        if stock >= cart.product_stock:
            cart.save()
        
        # calculating subtotal
        cartid = Cart.objects.filter(username=request.user)
        total = 0
        for i in cartid:
            if i.product_id.discount_price == None:
                total = i.product_id.price * i.product_stock
                print(total, "________________")
                # cart = Cart()
                i.sub_total = total
                i.save()
            else:
                total = i.product_id.discount_price * i.product_stock
                i.sub_total = total
                i.save()
        data = Cart.objects.get(product_id=id,username = request.user)
        
        # grand total
        cart_by_user = Cart.objects.filter(username=request.user)
        total = 0 
        grand_total = 0
        tax = 0
        for x in cart_by_user:
            if x.product_id.discount_price == None:
                total = x.product_id.price * x.product_stock
                grand_total += total 
                tax = (grand_total/100)*5
            else:
                total = x.product_id.discount_price * x.product_stock
                grand_total += total 
                tax = (grand_total/100)*5

        return JsonResponse({"product_stock": data.product_stock, "sub_total": data.sub_total, "grandtotal": grand_total, 'tax': tax})


# product decrement in cart
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_decrement(request):
    if request.method == 'POST':
        id = request.POST['id']
        
        #product stock decrementing
        cart = Cart.objects.get(product_id=id, username = request.user)
        cart.product_stock -= 1
        cart.save()
        cartid = Cart.objects.filter(username=request.user)
        total = 0
        for i in cartid:
            if i.product_id.discount_price == None:
                total = i.product_id.price * i.product_stock
                i.sub_total = total
                i.save()
            else:
                total = i.product_id.discount_price * i.product_stock
                i.sub_total = total
                i.save()

        data = Cart.objects.get(product_id=id,username = request.user)
       

        # grand total
        cart_by_user = Cart.objects.filter(username=request.user)
        item = 0
        stock = 0
        total = 0
        grand_total = 0
        tax = 0   
        for x in cart_by_user:
            if x.product_id.discount_price == None:
                item += x.product_id.price
                stock += x.product_stock
                total = x.product_id.price * x.product_stock
                grand_total += total
                tax = (grand_total/100)*5
            else:
                item += x.product_id.price
                stock += x.product_stock
                total = x.product_id.discount_price * x.product_stock
                grand_total += total
                tax = (grand_total/100)*5
        return JsonResponse({"product_stock": data.product_stock, "sub_total": data.sub_total, "grandtotal": grand_total, 'tax': tax})


#checkout view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request,id):
    try:
        coupon = request.GET['couponde']
    except:
        coupon = None
    
    cart = Cart.objects.filter(username = request.user.id)
    prdcts = 0
    for c in cart:
        prdcts = c.product_stock
    if prdcts == 0:
        return redirect(home)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(username = request.user)
        a_dict = {}
        total = 0
        grand_total = 0
        normal = 0
        for c in cart:
            if c.product_id.discount_price == None:
                total = c.product_id.price * c.product_stock
                a_dict[c.product_id.productname] = (total)
                grand_total += total
            else:
                total = c.product_id.discount_price * c.product_stock
                a_dict[c.product_id.productname] = (total)
                grand_total += total
        if coupon:
            normal = grand_total
            code = Coupon.objects.filter(coupon_code= coupon)
            for i in code:
                percentage = i.percentage
            discount_price = (grand_total * percentage)/100
            grand_total = round(grand_total - discount_price)

        #address displaying
        addrs = Address.objects.filter(user = id).order_by('-id')[:3]
        
        return render(request,'user_checkout.html',{'grandtotal':grand_total, 'product':cart, 'total':a_dict.items(),'address':addrs,'normal_orice':normal,'coupon_code':coupon})
    else:
        return render(request,'user_login.html')
