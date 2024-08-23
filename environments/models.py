from uuid import uuid4

from django.db import models

from common.models import TimestampMixin


# Create your models here.


class Environment(TimestampMixin):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name
