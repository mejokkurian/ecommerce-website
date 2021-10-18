from django.db import models
from django.db.models.deletion import CASCADE
from user.models import MyUser
from cart.models import Cart

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True)
    full_name = models.CharField(max_length=25)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=50) 
    date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    username = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    total = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)






