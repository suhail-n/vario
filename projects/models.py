from uuid import uuid4

from django.db import models
from django.urls import reverse

from environments.models import Environment


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"uuid": self.uuid})

    @property
    def featureflag_set(self) -> models.QuerySet["FeatureFlag"]:
        return FeatureFlag.objects.filter(project=self)


class FeatureFlag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    @property
    def toggle_set(self) -> models.QuerySet["Toggle"]:
        return Toggle.objects.filter(feature_flag=self)


class Toggle(models.Model):
    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.feature_flag.name} - {self.environment.name} - {"ON" if self.enabled else "OFF"}"
