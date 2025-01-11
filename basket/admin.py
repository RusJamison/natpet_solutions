from django.contrib import admin
from .models import Basket, BasketItem
# Register your models here.


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__user__username']


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['basket', 'product', 'quantity', 'created_at']
    list_filter = ['basket', 'product']
    search_fields = ['basket__pk', 'product__name']

