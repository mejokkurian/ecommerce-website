from cart.models import Cart
from user.models import MyUser
from newadmin.models import category
from user.models import whishlist

def carts(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(username = request.user).count()
        print(cart_items)
        return {'CART_ITEMS':cart_items }
    elif request.session.has_key('guest_user'):
        guest_user =  request.session['guest_user']
        cart_items = Cart.objects.filter(guest_token = guest_user).count()
        return{'CART_ITEMS':cart_items}

    else:
        return{'CART_ITEMS':0}


def wish_list(request):
    if request.user.is_authenticated:
        whish_items = whishlist.objects.filter(user_name = request.user).count()
        return{'Whish_items': whish_items}
    else:
        return{'Whish_items':0}

def cat(request):
    cats = category.objects.all()
    return {'cat': cats}


