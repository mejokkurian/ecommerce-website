from os import name
from django.urls import include, path
from .import views

urlpatterns = [
    path('',views.address,name='address')
    
]

