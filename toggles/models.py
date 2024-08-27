from typing import TYPE_CHECKING
from typing import Any
from typing import Union

from django.db import models

from common.models import TimestampMixin


if TYPE_CHECKING:
    from environments.models import Environment
    from feature_flags.models import FeatureFlag


# Create your models here.
class Toggle(TimestampMixin):
    feature_flag: models.ForeignKey["FeatureFlag", Union["FeatureFlag", Any]] = (
        models.ForeignKey("feature_flags.FeatureFlag", on_delete=models.CASCADE)
    )
    environment: models.ForeignKey[
        "Environment", Union["Environment", models.Field]
    ] = models.ForeignKey("environments.Environment", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.feature_flag.name} - {self.environment.name} - {"ON" if self.enabled else "OFF"}"
