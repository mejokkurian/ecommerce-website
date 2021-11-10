import json
from typing import Set
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.messages.api import success
from django.db.models.deletion import SET_NULL
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.exceptions import RequestDataTooBig
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from .models import Product_offer, subcategory
from collections import Counter
from order.models import Order
from user.models import MyUser
from cart.models import Cart
from .models import category
from .models import Product
from .models import Coupon
from .models import user_coupon
from .models import Categoryoffer
from .models import brand
from .models import BannerUpdate
import base64
import datetime
from datetime import date
import io

from django.db.models import Avg, Count, Min, Max, Sum,FloatField
from datetime import datetime
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc

from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



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
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        admin = authenticate(username=username, password=password)

        if admin is not None:
            if admin.is_superuser:
                login(request, admin)
                return redirect(admin_home)
            else:
                messages.error(request, "Incorrect email or password!!!")
                return redirect(admin_login)
        else:
            messages.error(request, "Incorrect email or password!!!")
            return redirect(admin_login)
    else:
        if request.user.is_authenticated:
            u = 0
            toatal_order = Order.objects.all().count()
            total_products = Product.objects.all().count()
            print(total_products)
            k = Order.objects.aggregate(total_price=Sum('total'))
            total_sales = (k.values())
            new = k['total_price']

            orders_per_day = Order.objects.annotate(order_day=Trunc('date', 'day', output_field=DateTimeField())).values('order_day').annotate(orders=Count('id')).order_by('-order_day')[:10]
            ord_val_per_day = Order.objects.annotate(order_day=Trunc('date', 'day', output_field=DateTimeField())).values('total').annotate(ord_value=Sum('id')).order_by('-order_day')[:10]
            

            labels = []
            ord_data = []
            val_data = []


            for ord in orders_per_day:
                print(ord['order_day'], ord['orders'])
                labels.append(str(ord['order_day'].date()))
                ord_data.append(ord['orders'])

            for val in ord_val_per_day:
                val_data.append(int(val['ord_value']))
            
            print(val_data)
            
            print(labels)   
            print(ord_data)
            labels.reverse()
            orders_details = Order.objects.all().order_by('-date')[:5]

            context = {
                'labels':labels,
                'data':ord_data,
                'val_data':val_data,
                'toatal_order': toatal_order, 
                'total_products': total_products, 
                'total_sales': new,
                'orders_details':orders_details

                }

            return render(request, 'page-index-1.html', context)
        else:
            return redirect(admin_login)


# user list
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    users = MyUser.objects.all()
    return render(request, 'page-user-1.html', {'users': users})




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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_add_product(request):
    productname = request.POST['productname']
    discrptin = request.POST['discrptin']
    image1 = request.POST['pro_img1']
    image2 = request.POST['pro_img2']
    image3 = request.POST['pro_img3']
    image4 = request.POST['pro_img4']

    format, img1 = image1.split(';base64,')
    ext = format.split('/')[-1]
    img_data1 = ContentFile(base64.b64decode(
        img1), name=productname + '1.' + ext)

    format, img1 = image2.split(';base64,')
    ext = format.split('/')[-1]
    img_data2 = ContentFile(base64.b64decode(
        img1), name=productname + '1.' + ext)

    format, img1 = image3.split(';base64,')
    ext = format.split('/')[-1]
    img_data3 = ContentFile(base64.b64decode(
        img1), name=productname + '1.' + ext)

    format, img1 = image4.split(';base64,')
    ext = format.split('/')[-1]
    img_data4 = ContentFile(base64.b64decode(
        img1), name=productname + '1.' + ext)

    Category = category.objects.get(id=request.POST['Category'])
    Sub_category = subcategory.objects.get(id=request.POST['Sub_category'])
    Brand = brand.objects.get(id=request.POST['Brand'])
    stock_qnty = request.POST['stock_qnty']
    product_price = request.POST['product_price']
    

    products = Product.objects.create(
        productname=productname,
        description=discrptin,
        image=img_data1,
        image1=img_data2,
        image2=img_data3,
        image3=img_data4,
        category_name=Category,
        sub_catagory_name=Sub_category,
        brand_name=Brand,
        amount_in_stock=stock_qnty,
        price=product_price)
    products.save()

    messages.success(request, 'product added ')
    return redirect(add_product)
# admin product edit end


# admin product delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def product_delete(request):
    id = request.POST['id']
    products = Product.objects.get(id=id)
    products.delete()
    err = "error"
    return JsonResponse({'err':err})


# product catogary page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_catagory(request):
    catgry = category.objects.all()
    return render(request, 'product_categories.html', {'category': catgry})


# category creations
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_delete(request):
    print("eneter")
    id = request.POST['id']
    catgr_dlt = category.objects.get(id=id)
    catgr_dlt.delete()
    succ = "success"
    return JsonResponse({'success' :succ})


# subcategory page views
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sub_catogery(request):
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    return render(request, 'sub_category.html', {'catgs': catgs, 'subcatgry': subcatgry})


# create subcategory
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def subcat_delete(request):
    id = request.POST['id']
    subcatgry = subcategory.objects.get(id=id)
    subcatgry.delete()
    succ = "success"
    return JsonResponse({'success' : succ})


# brand creations
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brands(request):
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    brandsss = brand.objects.all()
    return render(request, 'admin_brand.html', {'catgs': catgs, 'subcatgry': subcatgry, 'brands': brandsss})


# admin brand creations
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def brand_delete(request):
    id = request.POST['id']
    branddl = brand.objects.get(id=id)
    branddl.delete()
    succ = "success"
    return JsonResponse({'succ':succ})


# admin category edit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request, id):
    Category = category.objects.get(id=id)
    return render(request, 'edit_category.html', {'cats': Category})


# category edit submit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subcategory_edit(request, id):
    subs = subcategory.objects.get(id=id)
    return render(request, 'subcat_edit.html', {'subs': subs})



# subcat edit successfully
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brand_edit(request, id):
    Brand = brand.objects.get(id=id)
    return render(request, 'brand_edit.html', {'brand': Brand})



# brand edit submit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brand_eddit_submit(request, id):
    name = request.POST['name']
    slug = request.POST['slug']

    Brand = brand.objects.get(id=id)

    Brand.brand_name = name
    Brand.slug = slug
    Brand.save()
    messages.success(request, 'Sucessfully Edited Brand!!!')
    return redirect(brands)



# product edit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Edit_product(request, id):
    products = Product.objects.get(id=id)
    catgs = category.objects.all()
    subcatgry = subcategory.objects.all()
    brands = brand.objects.all()
    return render(request, 'edit_product.html', {'products': products, 'catgs': catgs, 'subcatgry': subcatgry, 'brands': brands})


# product edit and submit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_edit_submit(request, id):
    products = Product.objects.get(id=id)

    productname = request.POST['productname']
    discrptin = request.POST['discrptin']
    image1 = request.FILES.get('img1')
    image2 = request.FILES.get('img2')
    image3 = request.FILES.get('img3')
    image4 = request.FILES.get('img4')
    
    Category = category.objects.get(category_name=request.POST['Category'])
    Sub_category = subcategory.objects.get(
        sub_category_name=request.POST['Sub_category'])
    Brand = brand.objects.get(brand_name=request.POST['Brand'])
    stock_qnty = request.POST['stock_qnty']
    product_price = request.POST['product_price']


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
    products.amount_in_stock = stock_qnty
    products.save()
    messages.success(request, 'Sucessfully Edited products!!!')
    return redirect(product_list)


# Admin order managent
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_managment(request):
    orders_details = Order.objects.all().order_by('-date')
    paginator = Paginator(orders_details, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'adm_ordrmangment.html', {'order_dtl': page_obj})


# def offer management
def offer_manegment(request):
    coupon = Coupon.objects.all()
    return render(request,'admin_offer.html',{'coupon':coupon})


# coupon creation
def coupon_creation(request):
    coupon_code = request.POST['coupon_code']
    percentage = request.POST['coupon_value']
    coupon_dscr = request.POST['coupon_dscr']
    expiry = request.POST['expiry']
    min_amount = request.POST['min_amount']
    Coupon.objects.create(coupon_code = coupon_code, percentage = percentage, 
            description = coupon_dscr, min_rate = min_amount,expiry_date = expiry )
    messages.success(request,'Coupon created!!!')
    return redirect(offer_manegment)


# coupon deleting 
def coupon_dlt(request,id):
    Coupon.objects.get(id = id).delete()
    messages.success(request,'Coupon Deleted!!!')
    return redirect(offer_manegment)


# coupon validation checking
@csrf_exempt
def coupon_checking(request):
    if request.method == 'POST':
        coupon_cod = request.POST['couponCode']
        print(coupon_cod)
        is_true = Coupon.objects.filter(coupon_code= coupon_cod).exists()
        if is_true:
            print("sanam inde")
            code = Coupon.objects.filter(coupon_code= coupon_cod)
            for i in code:
                percentage = i.percentage
                min_amount = i.min_rate
                expiry_date = i.expiry_date
                id = i.id
                print(id)
        
                coupon = user_coupon.objects.filter(user_name = request.user)
                print(coupon)
                for c in coupon:
                    coupon_user_code = c.cpn_code.id
                    print(coupon_user_code,"user code")
                    if coupon_user_code == id:
                        error = "coupon code is aleredy used!!"
                        failer = 'failer'
                        return JsonResponse({"success":failer  , "error":error })

                current_datetime = date.today()

            cart_by_user = Cart.objects.filter(username=request.user)
            print(cart_by_user, 'totalitem')
            item = 0
            stock = 0 
            total = 0 
            grand_total = 0
            for x in cart_by_user:
                if x.product_id.discount_price == None:
                    total = x.product_id.price * x.product_stock
                    item += x.product_id.price
                    stock += x.product_stock
                    grand_total += total 
                else:
                    total = x.product_id.discount_price * x.product_stock
                    item += x.product_id.price
                    stock += x.product_stock
                    grand_total += total

            if min_amount < grand_total:
                if expiry_date > current_datetime:
                    print(grand_total)
                    discount_price = (grand_total * percentage)/100
                    coupon_offer = round(grand_total - discount_price)
                    success = 'success'
                    return JsonResponse({"success": success, "discount_price":discount_price, "coupon_offer":coupon_offer})
                else:
                    error = "coupon code is expired!!"
                    failer = 'failer'

                    return JsonResponse({"success":failer  , "error":error })
            else:
                error = "coupon code is not valid!!"
                failer = 'failer'
                return JsonResponse({"success":failer  , "error":error })
        else:
            print("sanam illa")
            error = "coupon code is not valid!!"
            failer = 'failer'
            return JsonResponse({"success":failer  , "error":error })
           

# admin product offer
@csrf_exempt
def product_offer(request):
    product = Product.objects.all()
    print(product)
    prdct = Product_offer.objects.all() 

    if request.method == 'POST':
        print("enterd")
        offername = request.POST['offer_name']
        offervalue = request.POST['offer_value']
        productname = request.POST['product_name']
        expiry = request.POST['expiry']
        
        #taking integer from string
        id = []
        for word in productname.split():
            if word.isdigit():
                id.append(int(word))
        print(id)

        # convering string to integer// product id converted
        strings = [str(integer) for integer in id]
        a_string = "".join(strings)
        prdId = int(a_string)
        product_id = Product.objects.get(id = prdId)
        product_offer = Product_offer.objects.create(product = product_id, offer_name = offername, discount_value = offervalue , expiry_date=expiry)
        prdct = Product_offer.objects.all() 
        for p in prdct:
            offer_name = p.offer_name
            offer_value = p.discount_value
            prdct_name = p.product.productname

        # discount price adding to the product
        prd = Product.objects.filter(id = prdId)
        for j in prd:
            prdct_price = j.price
            percentage = (prdct_price*offer_value)/100
            discount_price = prdct_price - percentage
            j.discount_price = discount_price
            j.offer_name = offername
            j.save()
        return JsonResponse({"offrname": offer_name,"offer_value":offer_value,"prdct_name":prdct_name})
    
    return render(request,'product_offer.html',{'product': product,"offer": prdct})

# produt offer delete
@csrf_exempt
def prd_offer_dlt(request):
    id = request.POST['id']
    offer_dlt = Product_offer.objects.filter(id = id)
    
    for i in offer_dlt:
        prd_id = i.product.id

    #deleting offer field from product model    
    product = Product.objects.filter(id = prd_id)
    for p in product:
        p.discount_price = None
        p.offer_name = None
        p.save()
    
    Product_offer.objects.get(id = id).delete()
    messages.success(request,"product offer deleted")
    suuc = "success"
    return JsonResponse({'suuc':suuc})

# catogory offer
@csrf_exempt
def catogory_offer(request):
    catg = category.objects.all()
    catgry_offer = Categoryoffer.objects.all()
    if request.method == 'POST':
        offer_name = request.POST['offer_name']
        offer_value = request.POST['offer_value']
        catgryName = request.POST['catgryName']
        expiry = request.POST['expiry']
        print(offer_name)
        print(offer_value)
        print(catgryName)
        print(expiry)
        cats = category.objects.filter(category_name = catgryName)
        id = 0
        for cat in cats:
            id = cat.id
            catgry = category.objects.get(id = id)
        Categoryoffer.objects.create(categoryName = catgry, offerName = offer_name, discountPercentage = offer_value, expiry = expiry)
        success = "Offer Created successfully"

        catgry_ofr = Categoryoffer.objects.filter(offerName = offer_name)
        for cgry in catgry_ofr:
            value = cgry.discountPercentage
        
        products = Product.objects.filter(category_name = catgry)
        for prd in products:
            discount = 0
            discount = prd.price - (prd.price * value/100)
            print(discount)
            # checking discount price none or not 
            if prd.discount_price == None:
                prd.discount_price = discount
                prd.offer_name = offer_name
                prd.save()
            # checking discount price greater than discout value
            elif prd.discount_price > discount:
                prd.discount_price = discount
                prd.offer_name = offer_name
                prd.save()

            else:
                print("not saved")
        return JsonResponse({'successca':success})

    return render(request,"category_offer.html",{'category':catg, 'catgry_offer':catgry_offer})


# category offer delete
@csrf_exempt
def ctgry_offer_dlt(request):
    id = request.POST['id']
    offer = Categoryoffer.objects.filter(id = id)
        
    for k in offer:
        value = k.discountPercentage 
        cat_id = k.categoryName.id

        products = Product.objects.filter(category_name = cat_id)
        for p in products:
            discount = 0
            discount = p.price - (p.price * value/100)
            # product price checking and deleting
            if p.discount_price == None:
                pass
            elif p.discount_price == discount:
                p.discount_price = None
                p.offer_name = None
                p.save()
    offer.delete()
    messages.success(request,"Category offer deleted!!!")
    succ = "success"
    return JsonResponse({'succ':succ})


# pdf downloader 
@csrf_exempt
def pdf_download(request):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=letter, bottomup = 0)
    p.drawString(100, 100, "")
    textob = p.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    orders = Order.objects.all()[:10]

    lines = ["username    |    phone       |         status      |        total          |       order no         "]
   
    
   
    for ord in orders:
        lines.append(str(ord.username.username)+"   |    "+str(ord.phone)+"    |    "+ str(ord.status)+"    |    "+str(ord.total)+"    |      "+str(ord.order_number.order_no))
      
    print(lines,"\n")
    
    for line in lines:
        print(line, "\n")
        textob.textLine(str(line))

    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='details.pdf')


#sales report
def sales_reprt(request):
    if request.method == "POST":
        print("setup")
        frm = request.POST['from']
        to = request.POST['to']
        print(frm,to)
        orders_details = Order.objects.filter(date__range=(frm, to))
        return render(request,'sales_repot.html',{'orders_details':orders_details})
    else:
        print("moonji")
        orders_details = Order.objects.all().order_by('-date')
        paginator = Paginator(orders_details, 10)
        page_number = request.GET.get('page')
        return render(request,'sales_repot.html',{'orders_details':orders_details})


# banners 
def banners(request):
    banners = BannerUpdate.objects.all()
    return render(request,'banners.html', {'banners':banners})


# banners submit
def banners_submit(request):
    bannerName = request.POST['banner_name']
    pic = request.FILES['pic']
    expiry = request.POST['expiry']

    BannerUpdate.objects.create(banner_image = pic, banner_name = bannerName, expiry =  expiry)
    return redirect(banners)


# banner delete
def banner_dlt(request,id):
    BannerUpdate.objects.get(id = id).delete()
    return redirect(banners)


    