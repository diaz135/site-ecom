import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum([item.sub_total() for item in cart_items])
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        # Paiement par carte (Stripe)
        if payment_method == 'card':
            source = request.POST.get('stripeToken', None)
            if not source:
                messages.error(request, "Le paiement Stripe a échoué. Veuillez réessayer.")
                return redirect('orders:checkout')

            try:
                stripe.Charge.create(
                    amount=int(total * 100),  # en centimes
                    currency="xof",
                    description="IslamicStore - Paiement client",
                    source=source
                )
            except stripe.error.StripeError as e:
                messages.error(request, f"Erreur Stripe : {e.user_message}")
                return redirect('orders:checkout')

        # Création de la commande
        order = Order.objects.create(
            user=request.user,
            total=total,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            country=country,
            payment_method=payment_method,
            is_paid=(payment_method != 'cod')  # payé sauf pour COD
        )

        # Enregistrement des produits dans la commande
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Vider le panier
        cart_items.delete()

        return render(request, 'orders/thankyou.html', {'order': order})

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})


def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def terms(request):
    return render(request, 'store/terms.html')

def privacy(request):
    return render(request, 'store/privacy.html')

