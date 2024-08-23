from django.db import models
from django.utils import timezone


# Create your models here.
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
