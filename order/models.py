from django.db import models
from django.db.models.deletion import CASCADE
from user.models import MyUser
from cart.models import Cart
from newadmin.models import Product
from cart.models import Cartcopy
from newadmin.models import Coupon

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    full_name = models.CharField(max_length=25)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=50) 
    date = models.DateTimeField(auto_now_add=True)



stauts_choices = (
    ("order_placed", "order placed"),
    ("item_shipped", "item shipped"),
    ("order_deliverd", "order deliverd"),
    ("order_cancelled", "order cancelled"),
 )


class Ordernumber(models.Model):
    order_no = models.CharField(max_length=50,default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    username = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=10)
    status = models.CharField(max_length=50 ,choices= stauts_choices, default="order placed",blank=True,null=True)
    total = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    product_stock = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    order_number = models.ForeignKey(Ordernumber,on_delete=models.CASCADE,default=0)
    





