from django.db import models

class ProductItemManager(models.Manager):

    def active(self):
        return self.filter(active=True)

    # def have_qty(self):
    #     return self.active().filter(quantity__gte=1)