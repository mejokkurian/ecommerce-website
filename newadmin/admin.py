from django.contrib import admin
from newadmin.models import category,subcategory,brand,Product

# Register your models here.

admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(brand)
admin.site.register(Product)