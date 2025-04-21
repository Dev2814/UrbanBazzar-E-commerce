from django.contrib import admin
from django.urls import path
from orders import views
from django.conf import settings
from django.conf.urls.static import static

app = 'orders'

urlpatterns = [
    path('success/', views.order_success, name='order_success'),
    path('confirm/', views.confirm_order, name='confirm_order'),
    path('orders/', views.order_list, name='order_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
