from os import name
from. import views
from django.urls import path

urlpatterns = [
    
    path('',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name = 'newadmin'),
    path('product_list',views.product_list,name= 'product_list'),
    path('user_list',views.user_list,name= 'user_list'),
    path('user_del/<int:id>',views.user_del,name= 'user_del'),
    path('user_deactive/<slug:username>',views.user_deactive,name= 'user_deactive'),
    path('user_active/<slug:username>',views.user_active,name= 'user_active'),
    path('admin_logout',views.admin_logout,name = "admin_logout"),
    path('add_product',views.add_product,name = 'add_product'),
    path('product_catagory',views.product_catagory, name='product_catagory'),
    path('create_category',views.create_category, name='create_category'),
    path('category_delete/<int:id>',views.category_delete,name= 'category_delete'),
    path('sub_catogery',views.sub_catogery,name= 'sub_catogery'),
    path('create_sub_category',views.create_sub_category,name= 'create_sub_category'),
    path('subcat_delete/<int:id>',views.subcat_delete,name= 'subcat_delete'),  
    path('brand',views.brands,name= 'brand'), 
    path('create_brand',views.create_brand,name= 'create_brand'), 
    path('brand_delete/<int:id>',views.brand_delete,name= 'brand_delete'),
    path('admin_add_product',views.admin_add_product,name = 'admin_add_product'),
    path('product_delete/<int:id>',views.product_delete,name='product_delete'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('category_edit_submit/<int:id>',views.category_edit_submit,name='category_edit_submit'),
    path('subcategory_edit/<int:id>',views.subcategory_edit,name='subcategory_edit'),
    path('subcatedit_submit/<int:id>',views.subcat_editsubmit,name='subcat_editsubmit'),
    path('brand_edit/<int:id>',views.brand_edit, name = 'brand_edit'),
    path('brand_eddit_submit/<int:id>',views.brand_eddit_submit, name = 'brand_eddit_submit'),
    path('Edit_product/<int:id>',views.Edit_product, name = 'Edit_product'),
    path('product_edit_submit/<int:id>',views.product_edit_submit, name = 'product_edit_submit')  
]