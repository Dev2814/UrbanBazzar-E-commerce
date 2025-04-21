from django.contrib import admin
from django.urls import path
from cart import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "cart"
urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'), 
] 

