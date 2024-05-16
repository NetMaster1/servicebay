from django.contrib import admin
from .models import Shop, Workshop, Brand, Status, Supplier

# Register your models here.
# Register your models here.
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

# Register your models here.
admin.site.register(Shop, ShopAdmin),
admin.site.register(Workshop, WorkshopAdmin),
admin.site.register(Brand, BrandAdmin),
admin.site.register(Status, StatusAdmin),
admin.site.register(Supplier, SupplierAdmin),