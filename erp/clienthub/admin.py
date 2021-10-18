from django.contrib import admin

from .models import ClientCategory, Client

@admin.register(ClientCategory)
class ClientTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'notes', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['name']
    list_per_page = 50
    autocomplete_fields = ['category']