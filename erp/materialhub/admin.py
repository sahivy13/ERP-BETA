from django.contrib import admin

from .models import ProductMaterialCategory, ProductMaterial

@admin.register(ProductMaterialCategory)
class ProductMaterialTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'aka', 'hazard', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['name']
    list_per_page = 50
    autocomplete_fields = ['category']