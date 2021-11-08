from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.



class MyUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',null =True, blank = True, default='profile_pics/default.png')


from newadmin.models import Product
class whishlist(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    user_name = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)