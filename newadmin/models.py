from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
import datetime
from user.models import MyUser


# Create your models here.


class category(models.Model):
    description = models.TextField(max_length=250)
    slug = models.CharField(max_length=100,unique=True)
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category_name

class subcategory(models.Model):
    description = models.TextField(max_length=250)
    slug = models.CharField(max_length=100,unique=True)
    sub_category_name = models.CharField(max_length=100)
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name

class brand(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100,unique=True)
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category_name = models.ForeignKey(subcategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name

    

class Product(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='pics',blank = True,null =True)
    image1 = models.ImageField(upload_to='pics',blank = True,null =True)
    image2 = models.ImageField(upload_to='pics',blank = True,null =True)
    image3 = models.ImageField(upload_to='pics',blank = True,null =True)
    productname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand_name = models.ForeignKey(brand,on_delete=models.CASCADE)
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    sub_catagory_name = models.ForeignKey(subcategory,on_delete=models.CASCADE)
    amount_in_stock = models.IntegerField(blank=True,default=0,help_text=("Amount in stock"))
    offer_name = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.productname

class Coupon(models.Model):
    min_rate = models.IntegerField()
    coupon_code = models.CharField(max_length=50,unique=True)
    percentage = models.PositiveIntegerField()
    expiry_date = models.DateField()
    description = models.CharField(max_length=50,blank=True)


class user_coupon(models.Model):
    user_name = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    cpn_code = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

class Product_offer(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=50)
    discount_value = models.PositiveIntegerField()
    expiry_date = models.DateField()



class Categoryoffer(models.Model):
    categoryName = models.ForeignKey(category,on_delete=models.CASCADE)
    offerName = models.CharField(max_length=50)
    discountPercentage = models.PositiveIntegerField()
    expiry = models.DateField()


class BannerUpdate(models.Model):
    banner_image    = models.ImageField(blank = True,upload_to = 'banner_images')
    banner_name     = models.CharField(max_length=50)
    expiry       = models.DateTimeField()
    created_at      = models.DateTimeField(auto_now_add=True)
 

    def _str_(self):
        return self.banner_name



        
        
        
    






