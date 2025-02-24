from django.contrib import admin
from .models import CouponUsage, Order, OrderItem, Coupon


# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
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
    list_display = ["pk", "order", "product", "quantity", "price"]
    list_filter = ["order", "product"]
    search_fields = ["order__pk", "product__name"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "valid_from", "valid_to", "active")
    search_fields = ("code",)
    list_filter = ("active", "valid_from", "valid_to")

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ("user", "coupon", "used_at")
    list_filter = ("user", "coupon", "used_at")



