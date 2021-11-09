from django.contrib import messages
from django.db.models.query_utils import RegisterLookupMixin
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, message
from django.http import JsonResponse
from newadmin.models import Product
from user.views import home
from .models import Address, Order, Ordernumber
from django.urls.conf import path
from user.models import MyUser
from cart.models import Cart
from cart.models import Cartcopy
from newadmin.models import Coupon
import datetime
import razorpay
from newadmin.models import user_coupon
from django.core.paginator import Paginator



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
@csrf_exempt
def address_dlt(request):
    print("enterd")
    id = request.POST['id']
    user_id = request.user.id
    print(user_id, 'userid')
    addrs_dlt = Address.objects.get(id=id)
    addrs_dlt.delete()
    succ = "succsess"
    return JsonResponse({'success' : succ})


# razorpay integration
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def Razorpay(request):
    try:
        addres = request.POST['address']
    except:
        addres = None

    error = "please select/create address!!!"
    if addres == None:
        return JsonResponse({"error":error})

    cartid = Cart.objects.filter(username=request.user)
    total = 0
    for i in cartid:
        if i.product_id.discount_price == None:
            total += i.product_id.price * i.product_stock
        else:
            total += i.product_id.discount_price * i.product_stock

    # coupon Checking
    try:
        coupon = request.POST['coupon']
    except:
        coupon = None

    if coupon:
        percentage = 0
        coupon_code = Coupon.objects.filter(coupon_code = coupon)
        for cop in coupon_code:
            percentage = cop.percentage
        discount_price = (total * percentage)/100
        total = (total - discount_price)
    
    # amount adding to razorpay
    amount = int(total)
    Amount = amount * 100
    print(amount)
    print(Amount)
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_LnJaBOrsdCtTO1", "Vm4994FD1pa8p7lCtSakntCL"))
    payment = client.order.create(
        {'amount': Amount, 'currency': order_currency})
    print(payment, 'payments')
    return JsonResponse({'payment': payment})


 


# order placed page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_placed(request):
    cartcopy1 = Cart.objects.filter(username=request.user.id)
    stock = 0
    for cart in cartcopy1:
        stock = cart.product_stock
    if stock == 0:
        print('FAILED')
        return redirect(home) 
    address_id = request.POST['flexRadioDefault']
    method = request.POST['flexRadio']
    
    try:
        coupon_code = request.POST['coupon_code']
    except:
        coupon_code = None

   
    
    # generate order no
    yr                  = int(datetime.date.today().strftime('%Y'))
    dt                  = int(datetime.date.today().strftime('%d'))
    mt                  = int(datetime.date.today().strftime('%m'))
    d                   = datetime.date(yr,mt,dt)
    current_date        = d.strftime("%Y%m%d")
    orderno = Ordernumber()

    orderno.save()
    orderno.order_no       = current_date + str(orderno.id)
    orderno.save()

    cartAddrs = Address.objects.filter(id=address_id)
    for x in cartAddrs:
        full_name = x.full_name
        state = x.state
        city = x.city
        phone = x.mobile
        pincode = x.pincode
    
    
    # decresing product stock when order placed
    cart = Cart.objects.filter(username=request.user.id)
    for i in cart:
        product = Product.objects.filter(
            amount_in_stock=i.product_id.amount_in_stock)
        for p in product:
            prdct_min = p.amount_in_stock - i.product_stock
            p.amount_in_stock = prdct_min
            p.save()
   
   # copying cart details to cart copy
    for c in cart:
        prdct_id = c.product_id
        user_name = c.username
        prdct_stock = c.product_stock
        sub_total = c.sub_total
        date = c.date
        copy_cart = Cartcopy.objects.create(product_id = prdct_id,username = user_name, product_stock = prdct_stock, sub_total = sub_total, date = date)
        copy_cart.save()
    Cart.objects.filter(username=request.user.id).delete()

   
   # adding cart detalis to order model
    ordered_products = Cartcopy.objects.filter(username = request.user.id)
    userid = MyUser.objects.get(id=request.user.id)
    p = 0
    c = 0
    total = 0
    grand_total =0
    for m in ordered_products:
        prdctid= m.product_id
        prdct_stock = m.product_stock

        # discount price checking
        if m.product_id.discount_price == None:
            total = m.product_id.price * m.product_stock
            grand_total += total
        else:
            total = m.product_id.discount_price * m.product_stock
            grand_total += total

    #coupon checking 
    if coupon_code:
        percentage = 0
        coupon = Coupon.objects.filter(coupon_code= coupon_code)
        for c in coupon:
            percentage = c.percentage
        discount_price = (grand_total * percentage)/100
        grand_total = (grand_total - discount_price)
            
        order_model = Order.objects.create(username=userid, product = prdctid, phone=phone, city=city,
                                            pincode=pincode, payment_method=method, status='order placed', total=grand_total, product_stock = prdct_stock,order_number = orderno)
        order_model.save()


    cartcopy = Cartcopy.objects.filter(username=request.user.id)
    cartcopy.delete()
      
    user_address = Address.objects.filter(id=address_id)
    
    # sending emails to user  
    user = MyUser.objects.get(username = request.user)  
    mail_subject = 'Order Placed!!'
    message = (f"Hi {user.username}\nThank you for your order..!! \nTotal amount: {total} ")
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    #coupon code adding to user table
    try:
        c_user = MyUser.objects.get(id = request.user.id)
        coupon = Coupon.objects.filter(coupon_code= coupon_code)
        
        for cop in coupon:
            cpid = cop.id
            coopen_id = Coupon.objects.get(id = cpid)
        User_coupon = user_coupon.objects.create(user_name = c_user, cpn_code = coopen_id,status = 'used' )
    except:
        return render(request, 'ordeer_conf.html', {'order_dtls': orderno.order_no , 'total': grand_total, 'user_address': user_address,})
    return render(request, 'ordeer_conf.html', {'order_dtls': orderno.order_no , 'total': grand_total, 'user_address': user_address,})


# order details page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def orders(request):
    if request.user.is_authenticated:
        orders_details = Order.objects.filter(
            username=request.user.id).order_by('-date')
        paginator = Paginator(orders_details, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        userdtl = MyUser.objects.filter(id = request.user.id)
        order_count = Order.objects.filter(username =  request.user.id).count()
        return render(request, 'order_details.html', {'order_dtl': page_obj,'userdtl':userdtl, 'order_count':order_count})
    else:
        messages.error(request,"please login or create an account!!")
        return redirect("login")

# user profile update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userprofile_upddate(request,id):
    pic = request.FILES['pic']
    
    name = request.POST['Name']
    email = request.POST['Email']
    mobile = request.POST['MobileNo']

    user = MyUser.objects.get(id = id)
    user.username = name
    user.email = email
    user.mobile_number = mobile
    user.profile_pic = pic
    user.save()
    return redirect(orders)


# order delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_dlt(request, id):
    order = Order.objects.get(id=id)
    order.status = 'cancelled'
    order.save()
    return redirect(orders)


# order status changing
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def order_status(request):
    status = request.POST.get('value')
    id = request.POST.get('id')

    order_status = Order.objects.filter(id=id)
    print(order_status)

    for i in order_status:
        i.status = status
        i.save()

    orderDtl = Order.objects.filter(id=id)

    for m in orderDtl:
        status = m.status
    return JsonResponse({'status': status})
