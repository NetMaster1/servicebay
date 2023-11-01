from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from app_reference.models import Shop, Workshop, Brand, Status, Supplier

# Create your models here.

class Item(models.Model):
    shop = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=250)
    brand_modified=models.ForeignKey(Brand, on_delete=models.DO_NOTHING, null=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, null=True)
    model = models.CharField(max_length=250)
    imei = models.CharField(max_length=250)
    created = models.DateField(auto_now_add=True)
    date_of_purchase = models.DateField(null=True)
    client = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    defect = models.TextField()
    comment = models.TextField(default='used')
    full_set = models.TextField(default='full seet')
    warranty = models.BooleanField(default=False)
    cheque = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    status = models.CharField(max_length=250)
    status_modified = models.ForeignKey(Status, on_delete=models.DO_NOTHING, null=True)
    status_updated = models.DateField(auto_now=True)
    delta_expiring=models.IntegerField(default=0)
    delta_shop_hold = models.IntegerField(default=0)
    delta_pending=models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)  # sorting by date
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.model


class Registry(models.Model):
    created = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.id


class RegistryLine(models.Model):
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE)
    shop = models.CharField(max_length=250, blank=True)
    user = models.CharField(max_length=250, blank=True)
    brand = models.CharField(max_length=250, blank=True)
    model = models.CharField(max_length=250, blank=True)
    imei = models.CharField(max_length=250, blank=True)
    date_of_delivery = models.CharField(max_length=250, blank=True)
    created = models.DateField(auto_now_add=True)
    date_of_purchase = models.DateField(null=True)
    # date_of_repair = models.DateTimeField(blank=True)
    client = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    defect = models.TextField()
    comment = models.TextField(default='used')
    full_set = models.TextField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)

    def __int__(self):
        return self.id

class RegistryShopHold(models.Model):
    created = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.id


class RegistryLineShopHold(models.Model):
    item_link_number = models.ForeignKey(Item, default=0, on_delete=models.CASCADE)
    registry_shop_hold = models.ForeignKey(RegistryShopHold, on_delete=models.CASCADE)
    # shop = models.CharField(max_length=250, blank=True)
    # user = models.CharField(max_length=250, blank=True)
    # brand = models.CharField(max_length=250, blank=True)
    # model = models.CharField(max_length=250, blank=True)
    # imei = models.CharField(max_length=250, blank=True)
    # date_of_delivery = models.CharField(max_length=250, blank=True)
    # created = models.DateField(auto_now_add=True)
    # date_of_purchase = models.DateField(null=True)
    # # date_of_repair = models.DateTimeField(blank=True)
    # client = models.CharField(max_length=250, blank=True)
    # phone = models.CharField(max_length=250, blank=True)
    # defect = models.TextField()
    # comment = models.TextField(default='used')
    # full_set = models.TextField(max_length=250, blank=True)
    # status = models.CharField(max_length=250, blank=True)

    def __int__(self):
        return self.id


class Status_change(models.Model):
    date_of_change = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)
    imei = models.CharField(max_length=250, blank=True)
    brand = models.CharField(max_length=250, blank=True)
    model = models.CharField(max_length=250, blank=True)

