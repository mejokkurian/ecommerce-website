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
    path('otp_verify',views.otp_verify,name = 'otp_verify')
    

]
 