from django.db import models
from .managers import DistributorManager

class DistributorCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Distributor(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(DistributorCategory, null=True, on_delete=models.SET_NULL)

    description = models.TextField(null= True, blank= True)
    notes = models.TextField(null= True, blank= True)

    # Add once TypeFinance model is created
    # type_finance = models.ForeignKey("TypeFinance", null=True, blank=True, on_delete=models.SET_NULL)

    objects = models.Manager()
    broswer = DistributorManager()

    class Meta:
        db_table = "Distributor"
        verbose_name_plural = 'Distributors'


    def __str__(self):
        return self.name
