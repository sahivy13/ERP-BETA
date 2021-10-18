from django.db import models
from django.conf import settings
from .managers import ProductItemManager

CURRENCY = settings.CURRENCY

class ProductItemCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(ProductItemCategory, null=True, on_delete=models.SET_NULL)
    part_number = models.CharField(max_length=150, unique=True, null=True, blank=True)
    brand = models.CharField(max_length=150, null=True, blank=True)

    weight = models.DecimalField(default=0.00, decimal_places=2, max_digits=11, null=True, blank=True)
    volume = models.DecimalField(default=0.00, decimal_places=2, max_digits=11, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    objects = models.Manager()
    broswer = ProductItemManager()

    class Meta:
        db_table = "productitem"
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name