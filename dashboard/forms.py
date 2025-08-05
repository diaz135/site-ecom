from django import forms
from store.models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'stock', 'image', 'is_available']

from django import forms
from accounts.models import Notification
from django.contrib.auth.models import User

class NotificationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), label="Client")

    class Meta:
        model = Notification
        fields = ['user', 'title', 'message']

class NotificationForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        required=False,
        label="Client spécifique (ou laisser vide pour tous)"
    )
    title = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
