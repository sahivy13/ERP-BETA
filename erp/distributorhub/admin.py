from django.contrib import admin

from .models import DistributorCategory, Distributor

@admin.register(DistributorCategory)
class DistributorTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'notes', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['name']
    list_per_page = 50
    autocomplete_fields = ['category']