from uuid import uuid4
from django.db import models

# Create your models here.


class Environment(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name
