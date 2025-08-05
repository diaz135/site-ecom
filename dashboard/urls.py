from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('add-product/', views.add_product, name='add_product'),
    path('create-notification/', views.create_notification, name='create_notification'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/update/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)