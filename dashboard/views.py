from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from orders.models import Order
from store.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def dashboard_home(request):
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.filter(is_superuser=False).count()
    latest_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'latest_orders': latest_orders,
    }
    return render(request, 'dashboard/dashboard_home.html', context)

from .forms import ProductForm
from django.contrib import messages

@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit ajouté avec succès !')
            return redirect('dashboard:dashboard_home')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

@user_passes_test(is_admin)
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']

            if user:
                # Notification ciblée
                Notification.objects.create(user=user, title=title, message=message)
                messages.success(request, f"Notification envoyée à {user.username}.")
            else:
                # Broadcast à tous les clients
                clients = User.objects.filter(is_superuser=False)
                bulk_notifs = [Notification(user=client, title=title, message=message) for client in clients]
                Notification.objects.bulk_create(bulk_notifs)
                messages.success(request, "Notification envoyée à tous les clients.")
            return redirect('dashboard:dashboard_home')
    else:
        form = NotificationForm()
    return render(request, 'dashboard/create_notification.html', {'form': form})


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders/order_list.html', {'orders': orders})

@login_required
@user_passes_test(is_superuser)
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return redirect('dashboard:order_list')