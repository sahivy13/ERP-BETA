from django.db import models
from .managers import ProducerManager

class ProducerCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Producer(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(ProducerCategory, null=True, on_delete=models.SET_NULL)

    description = models.TextField(null= True, blank= True)
    notes = models.TextField(null= True, blank= True)

    # Add once TypeFinance model is created
    # type_finance = models.ForeignKey("TypeFinance", null=True, blank=True, on_delete=models.SET_NULL)

    objects = models.Manager()
    broswer = ProducerManager()

    class Meta:
        db_table = "Producer"
        # verbose_name_plural = 'Producers'


    def __str__(self):
        return self.name