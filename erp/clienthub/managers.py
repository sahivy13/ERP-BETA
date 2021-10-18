from django.db import models

class ClientManager(models.Manager):

    def active(self):
        return self.filter(active=True)