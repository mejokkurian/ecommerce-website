from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from newadmin.models import Product
from django.contrib import messages
from django.http import request
from user.models import MyUser, whishlist
from twilio.rest import Client
from cart.models import Cart
from os import chmod
import random
import user
from newadmin.models import BannerUpdate
from .private import Services,Auth_token,Account_sid

# Create your views here.


# home page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    banners = BannerUpdate.objects.all()
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(username = request.user).count()
        return render(request, 'user_home.html', {'products': products,'cart_items': cart_items, 'banners':banners})
    else:
        return  render(request, 'user_home.html' , {'products': products})


# login page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user_page(request):
    if request.user.is_authenticated:
        print("home")
        return redirect(home)
    else:
        return render(request, 'user_login.html')


# register pager view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    return render(request, 'user_register.html')



# user accont creation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_register(request):
    print('entered')
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password1 = request.POST['user_password']
        mail = request.POST['user-email']
        phone = request.POST['user-phone']

        if MyUser.objects.filter(username=user_name):
            messages.info(request, 'Username already taken')
            return redirect(register)
        elif MyUser.objects.filter(email=mail):
            messages.info(request, 'Eamil already taken ')
            return redirect(register)
        elif MyUser.objects.filter(mobile_number=phone):
            messages.info(request, 'Please enter a valid phone number')
            return redirect(register)

    user = MyUser.objects.create_user(
        username=user_name, password=password1, email=mail, mobile_number=phone)
    user.save()
    print(user)
    messages.success(request, 'Sucessfully created a account!!!')
    return redirect(login_user_page)



# user auth and login to home page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == 'POST':
        userName = request.POST['user_name']
        userEmail = request.POST['user_password']
        user = authenticate(username=userName, password=userEmail)

        if user is not None:
            login(request, user)
            gues_handeler(request)
            return redirect(home)
        else:
            messages.error(request, 'invalid credentilas')
            return redirect(login_user_page)

def gues_handeler(request):
    print("keri")
    if request.session.has_key('guest_user'):
        guest_id = request.session['guest_user']
        carteii = Cart.objects.filter(guest_token =guest_id)
        print(carteii)
        for k in carteii:
            print("hhhhh")
            id = k.product_id
            k.username = request.user
            k.guest_token = None

            v = Cart.objects.filter(product_id=id, username = request.user).first()
            if v:
                print("product already in cart")
            else:
                print("pinnem keri")
                k.save()
        del request.session['guest_user']


# user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect(login_user_page)


# user product view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_product_view(request, id):
    products = Product.objects.get(id=id)
    Products = Product.objects.all()
    return render(request, 'user_single_product.html', {'products': products, 'Products': Products})



# forgot password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Forget_password(request):
    return render(request,'forget_pass.html')


#otp verification
def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        print(otp ,'otp come')
        mobile = request.session['mobile']
        user_mobile = '+91' + mobile

    #twilio code for otp generation
        account_sid = Account_sid
        auth_token = Auth_token
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                            .services(Services) \
                            .verification_checks \
                            .create(to=user_mobile, code=otp)

        print(verification_check.status)

        
        #checking otp is valid or not. If valid redirect home
        if verification_check.status == 'approved':
            print("verified")
            user_dtl = MyUser.objects.filter(mobile_number = mobile)# user details
            
            for u in user_dtl:
                username = u.username
                print(username)
                user = MyUser.objects.get(username=username)
                if user is not None:
                    login(request, user)
                    return redirect(home)
        else:
            print("enter erro")
            messages.error(request,'Invalid OTP')
            return render(request,'otp_vrify.html') 
           
    return render(request,'otp_vrify.html')


# otp registrsation 
def otp_login(request):
    mobile = request.POST['mobile_no']
    request.session['mobile'] = mobile
    print(mobile)
    user = MyUser.objects.filter(mobile_number = mobile)
    print(user)
    for m in user:
        if m.mobile_number == mobile:
            n = random.randint(111111,999999)
            print(n,'random')
            user_mobile = '+91' + mobile
    
            print(user_mobile)
        
            # Your Account Sid and Auth Token from twilio.com / console
            account_sid = Account_sid    
            auth_token = Auth_token
            client = Client(account_sid, auth_token) 
            verification = client.verify \
                     .services(Services) \
                     .verifications \
                     .create(to= user_mobile, channel='sms')

            print(verification.status)                                                 
            return redirect('otp_verify')

    messages.error(request,'invalid phone number')    
    return redirect(Forget_password)



# Men Category based product listing 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mens_cat(request,id):
    products = Product.objects.filter(category_name = id)
    return render(request,'mens_womens_car.html',{'products':products})


# usser password changing
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    return render(request,'password/changepassword.html')


# password submiting
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_submit(request):
    old_pass = request.POST['old_password'].strip()
    new_pass1 = request.POST['new_password2'].strip()

    user = MyUser.objects.filter(id = request.user.id)
    for u in user:
        name = u.username
        if authenticate(password = old_pass,username =name ):
            u.set_password(new_pass1)
            u.save()
        else:
            messages.error(request,'Your old password is wrong!!!')
            return redirect(change_password)
    messages.success(request,'Your password changed successfully!! login to continue shopping')
    return redirect(login_user_page)

    
# user wishlist 
@csrf_exempt
def wishlist(request):
    if request.user.is_authenticated:
        wish_list = whishlist.objects.filter(user_name = request.user.id)
        if request.method == 'POST':
            if request.user.is_authenticated:
                product_id = request.POST['id']
                user = MyUser.objects.get(id = request.user.id)
                produt = Product.objects.get(id = product_id)
                
                whislist = whishlist()
                whislist.product_id = produt
                whislist.user_name = user
                tItem = whishlist.objects.filter(product_id=produt, user_name = request.user).first()

                if tItem:
                    print('entered')
                else:
                    whislist.save()

                wish_items = whishlist.objects.filter(user_name = request.user).count()
                success = 'product added to wishlist!!!'
                return JsonResponse({'success': success,'wish_items':wish_items})
            else:
                error = "error"
                return JsonResponse({'error':error })
    else:
        messages.error(request,"please login!!")
        return redirect('login')

    return render(request,'whishlist.html',{'wish_list': wish_list})  



# wish list delete
@csrf_exempt
def whishlis_dlt(request):
    id = request.POST['id']
    whishlist.objects.get(id = id).delete()
    error = "error"
    return JsonResponse({'error':error })


#search 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    value = request.POST['value']
    print(value)
    data = Product.objects.filter(Q(productname__icontains=value)).order_by("id")
    prod = Product.objects.all()
    prd_count = prod.count()
    count=data.count()
    return render(request,'mens_cat.html',{'products' : data,"count":count, "prd_count" : prd_count})

    



