
from django.contrib import admin
from .models import Product, Category, Manufacturer
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = ['categories', 'manufacturer', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'model']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name',]