from django.db import models

class RFQManager(models.Manager):

    def active(self):
        return self.filter(active=True)