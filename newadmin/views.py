from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from user.models import MyUser
from .models import category
from .models import subcategory
from .models import brand
from .models import Product
# Create your views here.


# admin login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    else:
        return render(request, 'adminlogin.html')


# admin home page login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    print("hoi")
    if request.method == 'POST':
        print("hi")
        username = request.POST['user_name']
        password = request.POST['password']
        admin = authenticate(username=username, password=password)

        if admin is not None:
            print('trueeeeee')
            if admin.is_superuser:
                login(request, admin)
                return redirect(admin_home)
            else:
                print('falseeeeeeeeeee')
                messages.error(request, "Incorrect email or password!!!")
                return redirect(admin_login)
        else:
            print('incorrect')
            messages.error(request, "Incorrect email or password!!!")
            return redirect(admin_login)
    else:
        if request.user.is_authenticated:
            return render(request, 'page-index-1.html')
        else:
            return redirect(admin_login)


# user list
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    users = MyUser.objects.all()
    return render(request, 'page-user-1.html', {'users': users})


# admin user delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_del(request, id):
    user1 = MyUser.objects.get(id=id)
    user1.delete()
    return redirect(user_list)


# admin user deactivate
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_deactive(request, username):
    user2 = MyUser.objects.get(username=username)
    user2.is_active = False
    user2.save()
    return redirect(user_list)



# admin user active
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_active(request, username):
    user3 = MyUser.objects.get(username=username)
    user3.is_active = True
    user3.save()
    return redirect(user_list)


# admin logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def admin_logout(request):
    logout(request)
    return redirect(admin_login)



# add product page view
def add_product(request):
    catgry = category.objects.all()
    subcatgry = subcategory.objects.all()
    brandsss = brand.objects.all()
    return render(request, 'admin_add_product.html', {'catgs': catgry, 'subcatgry': subcatgry, 'brands': brandsss})



# admin product list
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_list(request):
    products = Product.objects.all
    return render(request, 'page-products-list.html', {'products': products})



# admin product adding
def admin_add_product(request):
    productname = request.POST['productname']
    discrptin = request.POST['discrptin']
    image1 = request.FILES.get('img1')
    print(image1)
    image2 = request.FILES.get('img2')
    image3 = request.FILES.get('img3')
    image4 = request.FILES.get('img4')
    Category = category.objects.get(id=request.POST['Category'])
    Sub_category = subcategory.objects.get(id=request.POST['Sub_category'])
    Brand = brand.objects.get(id=request.POST['Brand'])
    stock_qnty = request.POST['stock_qnty']
    product_price = request.POST['product_price']
    diccount_price = request.POST['diccount_price']

    products = Product.objects.create(
    productname=productname, 
    description=discrptin,
    image=image1,
    image1=image2,
    image2=image3,
    image3=image4, 
    category_name=Category,
    sub_catagory_name=Sub_category, 
    brand_name=Brand, 
    amount_in_stock=stock_qnty, 
    price=product_price, 
    discount_price=diccount_price)
    products.save()

    messages.success(request, 'product added ')
    return redirect(add_product)
# admin product edit end



# admin product delete
def product_delete(request, id):
    products = Product.objects.get(id=id)
    products.delete()
    return redirect(product_list)



# product catogary page view
def product_catagory(request):
    catgry = category.objects.all()
    return render(request, 'product_categories.html', {'category': catgry})


# category creations
def create_category(request):
    cat_name = request.POST['cat_name']
    slug = request.POST['slug']
    descr = request.POST['discr']

    sub_cat = category.objects.create(
        category_name=cat_name, slug=slug, description=descr)
    sub_cat.save()
    messages.success(request, 'Sucessfully created category!!!')
    return redirect(product_catagory)


# category delete
def category_delete(request, id):
    catgr_dlt = category.objects.get(id=id)
    catgr_dlt.delete()
    return redirect(product_catagory)


# subcategory page views
def sub_catogery(request):
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    return render(request, 'sub_category.html', {'catgs': catgs, 'subcatgry': subcatgry})


# create subcategory
def create_sub_category(request):
    catgry = category.objects.get(id=request.POST['category'])
    sub_name = request.POST['sub_name']
    sub_dicr = request.POST['sub_discr']
    sub_slug = request.POST['slug']

    sub_catgry = subcategory.objects.create(
        category_name=catgry, sub_category_name=sub_name, slug=sub_slug, description=sub_dicr)
    sub_catgry.save()
    messages.success(request, 'Sucessfully created Subcatagory!!!')
    return redirect(sub_catogery)


# def delete subCategory
def subcat_delete(request, id):
    subcatgry = subcategory.objects.get(id=id)
    subcatgry.delete()
    return redirect(sub_catogery)


# brand creations
def brands(request):
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    brandsss = brand.objects.all()
    return render(request, 'admin_brand.html', {'catgs': catgs, 'subcatgry': subcatgry, 'brands': brandsss})


# admin brand creations
def create_brand(request):
    catgry = category.objects.get(id=request.POST['category'])
    subcatgry = subcategory.objects.get(id=request.POST['subcategory'])
    brandname = request.POST['brand_name']
    slug = request.POST['slug']

    brandss = brand.objects.create(
        category_name=catgry, sub_category_name=subcatgry, brand_name=brandname, slug=slug,)
    messages.success(request, 'Sucessfully create Brand!!!')
    brandss.save()
    return redirect(brands)


# admin brand delete
def brand_delete(request, id):
    branddl = brand.objects.get(id=id)
    branddl.delete()
    return redirect(brands)


# admin category edit
def edit_category(request, id):
    Category = category.objects.get(id=id)
    return render(request, 'edit_category.html', {'cats': Category})


# category edit submit
def category_edit_submit(request, id):
    name = request.POST['name']
    discr = request.POST['dscrptn']
    slug = request.POST['slug']

    cat_edit = category.objects.get(id=id)

    cat_edit.description = discr
    cat_edit.category_name = name
    cat_edit.slug = slug
    cat_edit.save()
    messages.success(request, 'Sucessfully Edited Categories!!!')
    return redirect(product_catagory)


# subcat editpage
def subcategory_edit(request, id):
    subs = subcategory.objects.get(id=id)
    return render(request, 'subcat_edit.html', {'subs': subs})

# subcat edit successfully
def subcat_editsubmit(request, id):
    name = request.POST['name']
    discr = request.POST['dscrptn']
    slug = request.POST['slug']
    

    subcat = subcategory.objects.get(id=id)

    subcat.sub_category_name = name
    subcat.description = discr
    subcat.slug = slug
    subcat.save()
    messages.success(request, 'Sucessfully Edited Sub Categories!!!')
    return redirect(sub_catogery)


# admin brand edit
def brand_edit(request,id):
    Brand = brand.objects.get(id = id)
    return render(request,'brand_edit.html', {'brand':Brand})

# brand edit submit
def brand_eddit_submit(request, id):
    name = request.POST['name']
    slug = request.POST['slug']

    Brand = brand.objects.get(id = id)

    Brand.brand_name = name
    Brand.slug = slug
    Brand.save()
    messages.success(request, 'Sucessfully Edited Brand!!!')
    return redirect(brands)

# product edit
def Edit_product(request,id):
    products = Product.objects.get(id = id)
    # print("-...--", products)
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    brands = brand.objects.all()
    return render(request,'edit_product.html',{'products': products,'catgs':catgs, 'subcatgry':subcatgry,'brands':brands })


# product edit and submit
def product_edit_submit(request,id):
    products = Product.objects.get(id = id)

    productname = request.POST['productname']
    discrptin = request.POST['discrptin']
    image1 = request.FILES.get('img1')
    image2 = request.FILES.get('img2')
    image3 = request.FILES.get('img3')
    image4 = request.FILES.get('img4')
    print("------------img1----", image1)
    print("------------img2----", image2)
    print("------------img3----", image3)
    print("------------img4----", image4)
    
    Category = category.objects.get(category_name=request.POST['Category'])
    Sub_category = subcategory.objects.get(sub_category_name =request.POST['Sub_category'])
    Brand = brand.objects.get(brand_name=request.POST['Brand'])
    stock_qnty = request.POST['stock_qnty']
    product_price = request.POST['product_price']
    diccount_price = request.POST['diccount_price']

    products.productname = productname  
    products.description = discrptin

    if image1 == None:
        products.image = products.image
    else: 
        products.image = image1
    if image2 == None:
        products.image1 = products.image1
    else:
        products.image1 = image2

    if image3 == None:
        products.image2 = products.image2
    else:
        products.image2 = image3
    if image3 == None:
        products.image3 = products.image3
    else:
        products.image3 = image4

    products.brand_name = Brand
    products.category_name = Category
    products.sub_catagory_name = Sub_category
    products.price = product_price
    products.discount_price = diccount_price
    products.amount_in_stock = stock_qnty
    products.save()
    messages.success(request,'Sucessfully Edited products!!!')
    return redirect(product_list)



   
