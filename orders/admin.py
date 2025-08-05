from django.contrib import admin
from .models import Order, OrderItem
from django.core.mail import send_mail
from accounts.models import Notification

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'id')
    list_editable = ('status',)
    inlines = [OrderItemInline]

    fields = (
        'user', 'full_name', 'phone',
        'address', 'city', 'country',
        'total', 'payment_method', 'status', 'is_paid', 'created_at'
    )
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status == 'shipped':
                # Envoi email
                send_mail(
                    subject=f"Votre commande n°{obj.id} a été expédiée",
                    message=(
                        f"Bonjour {obj.user.username},\n\n"
                        f"Votre commande n°{obj.id} a été expédiée et sera livrée sous peu.\n\n"
                        f"Merci pour votre confiance."
                    ),
                    from_email=None,
                    recipient_list=[obj.user.email],
                    fail_silently=True
                )

                # Notification
                Notification.objects.create(
                    user=obj.user,
                    title="Commande expédiée",
                    message=f"Votre commande n°{obj.id} a été expédiée."
                )

            elif obj.status == 'delivered':
                Notification.objects.create(
                    user=obj.user,
                    title="Commande livrée",
                    message=f"Félicitations ! Votre commande n°{obj.id} a été livrée avec succès."
                )

            elif obj.status == 'annulee' or obj.status == 'canceled':
                Notification.objects.create(
                    user=obj.user,
                    title="Commande annulée",
                    message=f"Votre commande n°{obj.id} a été annulée. Contactez-nous pour plus d’informations."
                )
        super().save_model(request, obj, form, change)
