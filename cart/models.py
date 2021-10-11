from django.db import models
from newadmin.models import Product
from user.models import MyUser

# Create your models here.

class Cart(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    username = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)
    product_stock = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    sub_total = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    
      

