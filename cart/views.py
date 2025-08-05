from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Coupon
from django.contrib.auth.decorators import login_required



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 1}  # ← AJOUTÉ ICI
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = _cart_id(request)
    cart_items = CartItem.objects.filter(cart__cart_id=cart, active=True)

    total = 0
    quantity = 0
    discount = 0
    coupon_applied = None
    invalid_coupon = False

    for item in cart_items:
        total += item.product.price * item.quantity
        quantity += item.quantity

    # Traitement du coupon
    if request.method == "POST":
        code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            discount = (coupon.discount / 100) * total
            coupon_applied = coupon
        except Coupon.DoesNotExist:
            invalid_coupon = True

    grand_total = total - discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'discount': discount,
        'grand_total': grand_total,
        'coupon_applied': coupon_applied,
        'invalid_coupon': invalid_coupon,
    }

    return render(request, 'cart/cart.html', context)

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
