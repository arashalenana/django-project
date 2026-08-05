from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'total_amount', 'status', 'date_created']
    list_filter = ['status', 'date_created']
    search_fields = ['order_number', 'full_name', 'email']
    inlines = [OrderItemInline]