from uuid import uuid4

from django.db import models
from django.urls import reverse

from common.models import TimestampMixin
from feature_flags.models import FeatureFlag


# Create your models here.


class Project(TimestampMixin):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"uuid": self.uuid})

    @property
    def featureflag_set(self) -> models.QuerySet["FeatureFlag"]:
        return FeatureFlag.objects.filter(project=self)
