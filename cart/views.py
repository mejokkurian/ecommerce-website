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
        cartid = Cart.objects.filter(username=request.user).order_by('id')
        total = 0
        item = 0
        stock = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total, "________________")
            i.sub_total = total
            i.save()
            item += i.product_id.price
            stock += i.product_stock
        grand_total = item * stock
        tax = (grand_total/100)*5
        print(tax, 'tax')
        print(grand_total)

        return render(request, 'cart.html', {'products': cartid, 'grandtotal': grand_total, 'tax': tax})
    else:
        return render(request, 'cart.html')


# add product to cart
@csrf_exempt
def add_cart(request):
    print("buttton clicked")
    if request.method == 'POST':
        id = request.POST['id']
        print('-------', id)
        user = request.user
        product = Product.objects.get(id=id)
        if MyUser.objects.filter(username=user).exists():
            print(' user available', user)
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
                print('CART SAVE')
                cart.save()
        else:
            print('no user___', user)
            request.session['product'] = product.id
            request.session['product_stock'] = 1
            request.session['sub_total'] = product.price
        return JsonResponse({"success": "success"})



# delete prodcut from the cart
def cartitem_dlt(request, id):
    cart_items = Cart.objects.get(id=id)
    cart_items.delete()
    return redirect(cart_view)



 # product increment in cart
@csrf_exempt
def product_increment(request):
    if request.method == 'POST':
        id = request.POST['id']
        product = Product.objects.get(id=id)
        stock = product.amount_in_stock

        print(stock, "stock")

        cart = Cart.objects.get(product_id=id,username = request.user)

        cart.product_stock += 1
        if stock >= cart.product_stock:
            cart.save()
        cartid = Cart.objects.filter(username=request.user)
        total = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total, "________________")
            # cart = Cart()
            i.sub_total = total
            i.save()
        data = Cart.objects.get(product_id=id,username = request.user)
        a = data.product_stock
        b = data.sub_total
        print(a)
        print(b)

        # grand total
        cart_by_user = Cart.objects.filter(username=request.user)
        print(cart_by_user, 'totalitem')
        item = 0
        stock = 0
        for x in cart_by_user:
            item += x.product_id.price
            stock += x.product_stock
        grand_total = item * stock
        tax = (grand_total/100)*5
        print(tax, 'tax')

        print(item, stock, "full amount")
        print(grand_total, 'grand total')
        return JsonResponse({"product_stock": data.product_stock, "sub_total": data.sub_total, "grandtotal": grand_total, 'tax': tax})




# product decrement in cart
@csrf_exempt
def product_decrement(request):
    if request.method == 'POST':
        id = request.POST['id']
        cart = Cart.objects.get(product_id=id, username = request.user)
        print(cart, "++++++++")
        cart.product_stock -= 1
        cart.save()
        cartid = Cart.objects.filter(username=request.user)
        total = 0
        for i in cartid:
            total = i.product_id.price * i.product_stock
            print(total, "________________")
            # cart = Cart()
            i.sub_total = total
            i.save()
        data = Cart.objects.get(product_id=id,username = request.user)
        a = data.product_stock
        b = data.sub_total
        print(a)
        print(b)

        # grand total
        cart_by_user = Cart.objects.filter(username=request.user)
        print(cart_by_user, 'totalitem')
        item = 0
        stock = 0
        for x in cart_by_user:
            item += x.product_id.price
            stock += x.product_stock
        grand_total = item * stock
        tax = (grand_total/100)*5
        print(tax, 'tax')

        print(item, stock, "full amount")
        print(grand_total, 'grand total')
        return JsonResponse({"product_stock": data.product_stock, "sub_total": data.sub_total, "grandtotal": grand_total, 'tax': tax})


#checkout view
def checkout(request):
    cart = Cart.objects.filter(username = request.user)
    print(cart)
    price = 0
    stock = 0
    a_dict = {}
    total = 0
   
    for c in cart:
        price += c.product_id.price
        stock += c.product_stock
        total = c.product_id.price * c.product_stock
        a_dict[c.product_id.productname] = (total)
        print(total,'single')
        print(price,stock,total)
    grand_total = price * stock
    print(a_dict.values(),"dictionary values")
    # values = a_dict.values()
    # values_list = list(values)
    # print(values_list)
    print(grand_total)
    return render(request,'user_checkout.html',{'grandtotal':grand_total, 'product':cart, 'total':a_dict.items()})
