from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
        ('livree', 'Livrée'),
    ]

    PAYMENT_METHODS = [
        ('cod', 'Paiement à la livraison'),
        ('orange_money', 'Orange Money'),
        ('mtn_money', 'MTN Mobile Money'),
        ('card', 'Carte bancaire'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    # Informations de livraison
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True) 
    country = models.CharField(max_length=100, default="Côte d'Ivoire")

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

