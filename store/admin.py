from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, TryOnImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  

class TryOnImageInline(admin.TabularInline):
    model = TryOnImage
    extra = 0  

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_category', 'price', 'stock', 'get_vendor_name', 'brand_name', 'created_at', 'updated_at')
    search_fields = ('name', 'product_category__name', 'vendor__username') 

    inlines = [ProductImageInline, TryOnImageInline]

    def get_vendor_name(self, obj):
        return obj.vendor.username if obj.vendor else "No Vendor"

    get_vendor_name.short_description = 'Vendor'

    def has_add_permission(self, request):
        return request.user.is_authenticated and (request.user.role == 'vendor' or request.user.is_superuser)
