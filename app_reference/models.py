from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=250)
   
    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __int__(self):
        return self.id
    
class Workshop(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'workshop'
        verbose_name_plural = 'workshops'

    def __int__(self):
        return self.id
    
class Supplier(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'

    def __int__(self):
        return self.id
    

class Brand(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __int__(self):
        return self.id
    

class Status(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __int__(self):
        return self.id