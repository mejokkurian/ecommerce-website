from django.urls.conf import path
from .import views
from os import name


urlpatterns = [
    path('cart_view',views.cart_view,name = 'cart_view'),
    path('add_cart',views.add_cart, name='add_cart'),
    path('cartitem_dlt',views.cartitem_dlt, name='cartitem_dlt'),
    path('product_increment',views.product_increment, name='product_increment'),
    path('product_decrement',views.product_decrement, name='product_decrement'),
    path('checkout/<int:id>',views.checkout, name='checkout')
]
