from uuid import uuid4

# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

from common.models import TimestampMixin
from feature_flags.models import FeatureFlag


def validate_unique_project_name(value):
    if Project.objects.filter(name=value).exists():
        raise ValidationError("Project with this name already exists.")


class Project(TimestampMixin):
    name = models.CharField(
        max_length=100,
        blank=False,
        validators=[
            MinLengthValidator(3, message="Name must be at least 3 characters"),
            validate_unique_project_name,
        ],
        help_text="Enter a unique name.",
    )
    description = models.TextField(
        blank=True,
        help_text="Enter a brief description.",
    )
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"uuid": self.uuid})

    @property
    def featureflag_set(self) -> models.QuerySet["FeatureFlag"]:
        return FeatureFlag.objects.filter(project=self)
