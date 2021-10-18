from django.db.models.query_utils import RegisterLookupMixin
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from cart.models import Cart
from newadmin.models import Product
from user.models import MyUser
from .models import Address, Order


# Create your views here.


# address page views
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def address(request):
    if request.user.is_authenticated:
        return render(request, 'address.html')
    else:
        return render(request, 'user_login.html')


# user address creation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def address_submit(request, id):
    if request.method == 'POST':
        username1 = MyUser.objects.get(id=id)
        print(username1)
        fullname = request.POST['fullname']
        phone = request.POST['phone']
        pin = request.POST['pin']
        state = request.POST['state']
        city = request.POST['city']
        distr = request.POST['district']
        address = request.POST['address']

        address_crtn = Address.objects.create(user=username1, full_name=fullname, mobile=phone,
                                              pincode=pin, state=state, city=city, district=distr, address_line1=address)
        address_crtn.save()

        user_id = request.user.id
        print(user_id, 'userid')
        return redirect('checkout', id=user_id)
    else:
        return redirect('checkout', id=request.user.id)


# user adress delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def address_dlt(request, id):
    user_id = request.user.id
    print(user_id, 'userid')
    addrs_dlt = Address.objects.get(id=id)
    print(addrs_dlt, 'delete address')
    addrs_dlt.delete()
    return redirect(address_submit, id=user_id)


# order placed page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_placed(request, id):
    print(id, 'addressid')
    address_id = request.POST['flexRadioDefault']
    method = request.POST['flexRadio']
    print(method)
    print(address_id, 'value came')
    cartitem = Address.objects.filter(id=address_id)
    for x in cartitem:
        full_name = x.full_name
        state = x.state
        city = x.city
        phone = x.mobile
        pincode = x.pincode
    print(full_name, 'fullname')
    print(state, 'state')
    print(city, 'city')
    print(phone, 'phone')
    print(pincode, 'pin')

    cart_user = Cart.objects.filter(username=request.user.id)
    userid = MyUser.objects.get(id=request.user.id)

    total = 0
    for i in cart_user:
        print(i.product_id, 'product id')
        total += i.sub_total
        print(total, 'toal')
        order_model = Order.objects.create(username=userid, product=i, phone=phone, city=city,
                                           pincode=pincode, payment_method=method, status='pending', total=i.sub_total)
        order_model.save()
        print(i.product_stock, 'product stock')
    print(total, 'full total ')

    order_details = Order.objects.filter(username=request.user.id)
    for m in order_details:
        Total = 0
        Total += m.total
    user_address = Address.objects.filter(id=address_id)

    print(user_address)
    for k in user_address:
        a = k.state, 'address'
        b = k.district, 'address'
        c = k.pincode, 'address'
        print(a, b, c)

    cart = Cart.objects.filter(username = request.user.id )
    for i in cart:
        print(i.product_stock,'product stock' )
        print(i.product_id.amount_in_stock,'peoduct real stock')

        
        product = Product.objects.filter(amount_in_stock = i.product_id.amount_in_stock)
        for p in product:
            prdct_min = p.amount_in_stock - i.product_stock
            p.amount_in_stock= prdct_min
            p.save()

        
    cart1 = Cart.objects.filter(username = request.user.id ).delete()

        
    return render(request, 'ordeer_conf.html', {'order_dtls': order_details, 'total': Total, 'user_address': user_address})


# order details page
def orders(request):
    orders_details = Order.objects.filter(username = request.user.id)
    for o in orders_details:
        print(o.status)
    return render(request,'order_details.html',{'order_dtl': orders_details})

# order delete
def order_dlt(request,id):
    order = Order.objects.get(id = id)
    order.delete()
    return redirect(orders)
