from django.db import models

class ProductMaterialManager(models.Manager):

    def active(self):
        return self.filter(active=True)