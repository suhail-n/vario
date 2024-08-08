from django.contrib import admin

from .models import FeatureFlag
from .models import Project
from .models import Toggle


# Register your models here.


admin.site.register(Project)
admin.site.register(FeatureFlag)
admin.site.register(Toggle)
