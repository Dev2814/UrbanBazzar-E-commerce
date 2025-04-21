from django.contrib import admin
from .models import OrderDetails, OrderItems

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'payment')
    search_fields = ('user__email',)

admin.site.register(OrderDetails, OrderDetailsAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__email', 'product__name')

admin.site.register(OrderItems, OrderItemsAdmin)
