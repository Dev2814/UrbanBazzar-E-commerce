from django import forms
from .models import UserAddress, UserSecondaryAddress

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address', 'city', 'pincode', 'country', 'mobile']

class UserSecondaryAddressForm(forms.ModelForm):
    class Meta:
        model = UserSecondaryAddress
        fields = ['address', 'city', 'pincode', 'country', 'mobile']
