from django.contrib import admin

from .models import ClientItemRFQ, RFQItem

@admin.register(ClientItemRFQ)
class ProductItemTypeAdmin(admin.ModelAdmin):
    search_fields = ['rfq_number']
    list_filter = ['client', 'rfq_number', 'is_requested', 'is_quoted', 'is_ordered']
    list_display = ['client', 'rfq_number', 'is_requested', 'is_quoted', 'is_ordered']

@admin.register(RFQItem)
class ProductItemAdmin(admin.ModelAdmin):
    search_fields = ['rfq']
    list_display = ['rfq', 'product', 'quantity']
    list_select_related = ['product']
    list_filter = ['product']
    search_fields = ['name']
    list_per_page = 50
    autocomplete_fields = ['product']
