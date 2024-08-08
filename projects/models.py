from uuid import uuid4

from django.db import models
from django.urls import reverse

from environments.models import Environment


# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"uuid": self.uuid})


class FeatureFlag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name


class Toggle(models.Model):
    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
