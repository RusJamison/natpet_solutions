from django.contrib import admin
from .models import Order, Payment, OrderItem,Review
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'created_at', 'updated_at', 'status', 'total_amount']
    list_filter = ['customer', 'created_at', 'updated_at', 'status']
    search_fields = ['customer__user__username', 'shipping_address', 'billing_address']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__pk', 'product__name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order', 'amount', 'status', 'payment_method', 'transaction_id', 'created_at']
    list_filter = ['order', 'status', 'payment_method', 'created_at']
    search_fields = ['order__pk', 'transaction_id']
