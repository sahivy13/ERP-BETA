from django.db import models

class DistributorManager(models.Manager):

    def active(self):
        return self.filter(active=True)