from typing import TYPE_CHECKING
from typing import Union
from uuid import uuid4

from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.db import models

from categories.models import get_default_category
from common.models import TimestampMixin
from toggles.models import Toggle


if TYPE_CHECKING:
    from categories.models import Category
    from projects.models import Project


# Create your models here.
class FeatureFlag(TimestampMixin):
    project: models.ForeignKey["Project", int] = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        validators=[
            MinLengthValidator(3, message="Name must be at least 3 characters"),
            RegexValidator(
                r"^[a-zA-Z0-9_-]*$",
                message="Name must be only alphanumeric characters, underscores, and hypens are allowed",
            ),
        ],
    )
    enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    category: models.ForeignKey["Category", Union["Category", models.Field, None]] = (
        models.ForeignKey(
            "categories.Category",
            on_delete=models.SET_NULL,
            default=get_default_category,
            null=True,
        )
    )

    def __str__(self) -> str:
        return self.name

    @property
    def toggle_set(self) -> models.QuerySet[Toggle]:
        return Toggle.objects.filter(feature_flag=self)
