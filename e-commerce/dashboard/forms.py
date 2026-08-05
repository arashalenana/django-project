from django import forms
from products.models import Product, Category
from django.contrib.auth.models import Permission
from orders.models import Order

class DashboardProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'price', 'discount_price',
            'image', 'stock_quantity', 'is_available',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the product...'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Shoes'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean_discount_price(self):
        discount_price = self.cleaned_data.get('discount_price')
        if discount_price is not None and discount_price < 0:
            raise forms.ValidationError('Discount price cannot be negative.')
        return discount_price

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data['stock_quantity']
        if stock_quantity < 0:
            raise forms.ValidationError('Stock quantity cannot be negative.')
        return stock_quantity

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        if price is not None and discount_price is not None and discount_price > price:
            self.add_error(
                'discount_price',
                'Discount price should not be greater than the regular price.'
            )
        return cleaned_data

class DashboardCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description...'}),
        }

class DashboardUserPermissionsForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            content_type__app_label__in=['products', 'orders', 'authentication']
        ).select_related('content_type'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

class DashboardOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']