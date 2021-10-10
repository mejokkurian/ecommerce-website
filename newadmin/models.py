from django.db import models

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
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_catagory_name = models.ForeignKey(subcategory,on_delete=models.CASCADE)
    amount_in_stock = models.IntegerField(blank=True,default=0,help_text=("Amount in stock"))
    
    
    
    

    
        
        
        
    






