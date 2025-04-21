from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PaymentDetails

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'provider', 'status', 'created_at', 'updated_at')
    search_fields = ('order__user__email', 'provider')


admin.site.register(PaymentDetails, PaymentDetailsAdmin)
