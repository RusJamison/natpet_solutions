from django.contrib import admin
from .models import Order,  OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__pk', 'product__name']

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'order', 'amount', 'status', 'payment_method', 'transaction_id', 'created_at']
#     list_filter = ['order', 'status', 'payment_method', 'created_at']
#     search_fields = ['order__pk', 'transaction_id']