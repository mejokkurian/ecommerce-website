from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from newadmin.models import Product
from django.contrib import messages
from user.models import MyUser
from twilio.rest import Client
from cart.models import Cart
from os import chmod
import random

# Create your views here.


# home page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    products = Product.objects.all()
    
    return render(request, 'user_home.html', {'products': products})



# login page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user_page(request):
    if request.user.is_authenticated:
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
            return redirect(home)
        else:
            messages.error(request, 'invalid credentilas')
            return redirect(login_user_page)



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
        account_sid = 'ACab842a0b7a47d48921abd9e4e37f3b4b'
        auth_token = '5a92b7079a6eeb08689f9f6204c5a52e'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                            .services('VA20ee15ba9130b5a31bf11e2965517bb9') \
                            .verification_checks \
                            .create(to=user_mobile, code=otp)

        print(verification_check.status)

        
        #checking otp is valid or not. If valid redirect home
        if verification_check == 'approved':
            user_dtl = MyUser.objects.filter(mobile_number = mobile)# user details
            
            for u in user_dtl:
                username = u.username
                user = MyUser.objects.get(username=username)
                if user is not None:
                    login(request, user)
                    return redirect(home)
        else:
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
            account_sid = 'ACab842a0b7a47d48921abd9e4e37f3b4b'    
            auth_token = '5a92b7079a6eeb08689f9f6204c5a52e'
            client = Client(account_sid, auth_token) 
            verification = client.verify \
                     .services('VA20ee15ba9130b5a31bf11e2965517bb9') \
                     .verifications \
                     .create(to= user_mobile, channel='sms')

            print(verification.status)                                                 
            return redirect('otp_verify')

    messages.error(request,'invalid phone number')    
    return redirect(Forget_password)






    
    




