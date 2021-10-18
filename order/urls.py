from os import name
from django.urls import include, path
from .import views

urlpatterns = [
    path('',views.address,name='address'),
    path('address_submit/<int:id>',views.address_submit,name='address_submit'),
    path('address_dlt/<int:id>',views.address_dlt,name='address_dlt'),
    path('order_placed/<int:id>',views.order_placed,name='order_placed'),
    path('orders',views.orders,name='orders'),
    path('order_dlt/<int:id>',views.order_dlt,name='order_dlt')
    
]

    
