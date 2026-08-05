from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'delivery_address']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
        }