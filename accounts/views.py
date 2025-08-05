from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from orders.models import Order
from django.db.models import Sum
from .forms import ProfileForm
from .models import Profile
from accounts.models import Notification


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # ou tableau de bord
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Identifiants incorrects')
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('store:home')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})



@login_required
def client_dashboard(request):
    user_orders = Order.objects.filter(user=request.user)
    total_spent = user_orders.aggregate(Sum('total'))['total__sum'] or 0
    total_orders = user_orders.count()
    latest_orders = user_orders.order_by('-created_at')[:5]

    context = {
        'total_spent': total_spent,
        'total_orders': total_orders,
        'latest_orders': latest_orders,
    }
    return render(request, 'accounts/client_dashboard.html', context)

from django.shortcuts import get_object_or_404

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/order_detail.html', {'order': order})

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    template = get_template('accounts/invoice.html')
    html = template.render({'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/notifications.html', {'notifications': notifications})

@login_required
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user).delete()
        messages.success(request, "Toutes les notifications ont été supprimées.")
    return redirect('accounts:notifications_list')
