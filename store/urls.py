from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "store"

urlpatterns = [
    path('urbanbazzar/products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('vender-dashboard/', views.vender_dashboard, name='vender_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
