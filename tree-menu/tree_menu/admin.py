from django.contrib import admin
from .models import Menu, MenuItem

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name', 'title')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order', 'named_url', 'url')
    list_filter = ('menu',)
    search_fields = ('title', 'url', 'named_url')
    ordering = ('menu', 'order')
