from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('legal/', views.legal_mentions, name='legal_mentions'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),

]
