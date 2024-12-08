from django.contrib import admin
from .models import Item, Registry, RegistryLine, Status_change

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'brand', 'model', 'created', 'client', 'user', 'status')
    ordering = ('-id',)
    list_filter = ('status',)
    list_editable= ('status', )
    search_fields = ('imei', )

class RegistryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')

class RegistryLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model')

class Status_changeAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'imei')

# Register your models here.
admin.site.register(Item, ItemAdmin),
admin.site.register(Registry, RegistryAdmin),
admin.site.register(RegistryLine, RegistryLineAdmin),
admin.site.register(Status_change, Status_changeAdmin),


