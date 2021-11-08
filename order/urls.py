from os import name
from django.urls import include, path
from .import views

urlpatterns = [
    path('',views.address,name='address'),
    path('address_submit/<int:id>',views.address_submit,name='address_submit'),
    path('address_dlt',views.address_dlt,name='address_dlt'),
    path('order_placed',views.order_placed,name='order_placed'),
    path('orders',views.orders,name='orders'),
    path('order_dlt/<int:id>',views.order_dlt,name='order_dlt'),
    path('Razorpay',views.Razorpay,name='Razorpay'),
    path('order_status',views.order_status,name='order_status'),
    path('userprofile_upddate/<int:id>',views.userprofile_upddate,name='userprofile_upddate')
      
]

    
