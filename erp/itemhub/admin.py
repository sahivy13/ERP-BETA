from django.contrib import admin

from .models import ProductItemCategory, ProductItem

@admin.register(ProductItemCategory)
class ProductItemTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'part_number', 'brand', 'category', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['name']
    list_per_page = 50
    autocomplete_fields = ['category']
