from django import forms
from .models import Product, ProductImage
from django.forms import modelformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id' ,'name', 'brand_name', 'description', 'product_category', 'price', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Image form for one image
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

# Formset to handle multiple images
ProductImageFormSet = modelformset_factory(
    ProductImage,
    form=ProductImageForm,
    extra=1,          # Show one empty field initially
    can_delete=True   # Allow deletion
)