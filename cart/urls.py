from django.urls.conf import path
from .import views
from os import name


urlpatterns = [
    path('cart_view',views.cart_view,name = 'cart_view'),
    path('add_cart',views.add_cart, name='add_cart'),
    path('cartitem_dlt/<int:id>',views.cartitem_dlt, name='cartitem_dlt')
    
    
]
