from django.shortcuts import redirect, render
# from django.contrib.auth.models import MyUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import auth
from user.models import MyUser
from newadmin.models import Product
from django.views.decorators.cache import cache_control

# Create your views here.

# home page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    products = Product.objects.all()
    return render(request,'user_home.html',{'products': products})

# login page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user_page(request):
    return render(request,'user_login.html')


# register pager view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    return render(request,'user_register.html')

# user accont creation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_register(request):
    print('entered')
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password1 = request.POST['user_password']
        mail = request.POST['user-email']
        phone = request.POST['user-phone']

        if MyUser.objects.filter(username = user_name):
            messages.info(request, 'Username already taken')
            return redirect(register)
        elif MyUser.objects.filter(email = mail):
            messages.info(request, 'Eamil already taken ')
            return redirect(register)
        elif MyUser.objects.filter(mobile_number = phone):
            messages.info(request, 'Please enter a valid phone number')
            return redirect(register)
    
    user = MyUser.objects.create_user(username = user_name,password = password1,email = mail, mobile_number = phone)
    user.save()
    print(user)
    messages.success(request,'Sucessfully created a account!!!')
    return redirect(login_user_page)  

#user auth and login to home page
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
            messages.error(request,'invalid credentilas')
            return redirect(login_user_page)

# user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect(login_user_page)

# user product view
def user_product_view(request,id):
    products = Product.objects.get(id = id)
    Products = Product.objects.all()
    return render(request,'user_single_product.html',{'products':products, 'Products': Products})

def cart_view(request):
    return render(request,'cart.html')





    