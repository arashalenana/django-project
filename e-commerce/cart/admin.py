from django.contrib import admin
from .models import CartItem
# Register your models here.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'date_added']
    list_filter = ['date_added']
    search_fields = ['user__username', 'product__name']