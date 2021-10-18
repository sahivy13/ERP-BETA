from django.db import models

class ProducerManager(models.Manager):

    def active(self):
        return self.filter(active=True)