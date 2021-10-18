from django.db import models
from django.conf import settings
from .managers import ProductMaterialManager

CURRENCY = settings.CURRENCY

class ProductMaterialCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

# class PackageType(models.Model):
#     name = models.CharField(max_length=150, unique=True)

#     def __str__(self):
#         return self.name


class ProductMaterial(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(ProductMaterialCategory, null=True, on_delete=models.SET_NULL)
    aka = models.CharField(max_length=1024)

    hazard = models.BooleanField(default=False)
    # package = models.ForeignKey("PackageType", null=True, blank=True, on_delete=models.SET_NULL)
    # humidity = models.DecimalField(default=0.00, decimal_places=2, max_digits=11, null=True, blank=True)
    # density = models.DecimalField(default=0.00, decimal_places=2, max_digits=11, null=True, blank=True)
    # density_unity = models.ForeignKey("DensityUnit", null=True, blank=True, on_delete=models.SET_NULL)
    # granularity = models.DecimalField(default=0.00, decimal_places=2, max_digits=11, null=True, blank=True)
    # granularity_unit = models.ForeignKey("GranularityUnit", null=True, blank=True, on_delete=models.SET_NULL)
    # other_physical = models.TextField(null= True, blank= True)

    # producers = models.ManyToManyField("Producers", null=True, blank=True)
    # distributors = models.ManyToManyField("Distributors", null=True, blank=True)

    description = models.TextField(null= True, blank= True)


    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)

    objects = models.Manager()
    broswer = ProductMaterialManager()

    class Meta:
        db_table = "productmaterial"
        verbose_name_plural = 'Materials'

    # def save(self, *args, **kwargs):
    #     self.final_price = self.price if self.price > self.cost else self.cost
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name