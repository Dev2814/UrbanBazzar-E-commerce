from django.contrib import admin
from .models import ShoppingSession, CartItem

class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'total')
    search_fields = ('user__email',)

admin.site.register(ShoppingSession, ShoppingSessionAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('session', 'product', 'quantity')
    search_fields = ('session__user__email', 'product__name')

admin.site.register(CartItem, CartItemAdmin)
