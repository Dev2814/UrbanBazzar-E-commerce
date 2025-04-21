from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserAddress, UserSecondaryAddress, UserPayment

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_active')
    search_fields = ('email', 'username', 'role')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'pincode', 'country', 'mobile')
    search_fields = ('user__email', 'city', 'pincode')

admin.site.register(UserAddress, UserAddressAdmin)

class UserSecondaryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'pincode', 'country', 'mobile')
    search_fields = ('user__email', 'city', 'pincode')

admin.site.register(UserSecondaryAddress, UserSecondaryAddressAdmin)

class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_type', 'provider', 'account_no')
    search_fields = ('user__email', 'provider')

admin.site.register(UserPayment, UserPaymentAdmin)
