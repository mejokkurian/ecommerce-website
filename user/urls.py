from os import name
from django.urls import include, path
from .import views


urlpatterns = [
    path('',views.home,name='home'),
    path('login_user_page',views.login_user_page,name='login'),
    path('register',views.register,name = 'register'),
    path('user_register',views.user_register,name='user_register'),
    path('login_user',views.login_user,name = 'login_user'),
    path('user_logout',views.user_logout,name = 'user_logout'),
    path('user_product_view/<int:id>',views.user_product_view,name = 'user_product_view'),
    path('Forget_password',views.Forget_password,name = 'Forget_password'),
    path('otp_login',views.otp_login,name = 'otp_login'),
    path('otp_verify',views.otp_verify,name = 'otp_verify'),
    path('mens_cat/<int:id>',views.mens_cat,name = 'mens_cat'),
    path('change_password',views.change_password,name = 'change_password'),
    path('password_submit',views.password_submit,name = 'password_submit'),
    path('wishlist',views.wishlist,name = 'wishlist'),
    path('whishlis_dlt',views.whishlis_dlt,name = 'whishlis_dlt'),
    path('search',views.search,name = 'search')
    

]
