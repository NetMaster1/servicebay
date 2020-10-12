from django.contrib import admin
from .models import Item, Registry, RegistryLine

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'created', 'client')

class RegistryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')

class RegistryLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model')

# Register your models here.
admin.site.register(Item, ItemAdmin),
admin.site.register(Registry, RegistryAdmin),
admin.site.register(RegistryLine, RegistryLineAdmin)
