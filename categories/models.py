# Create your models here.
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampMixin


class Category(TimestampMixin):
    class CategoryChoices(models.TextChoices):
        RELEASE = "release", _("Release")
        OPERATIONAL = "operational", _("Operational")
        EXPERIMENTAL = "experiment", _("Experiment")
        KILL_SWITCH = "kill_switch", _("Kill Switch")
        PERMISSION = "permission", _("Permission")

    name = models.CharField(
        max_length=50, choices=CategoryChoices.choices, default=CategoryChoices.RELEASE
    )
    description = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name
