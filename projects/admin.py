from django.contrib import admin
from .models import Project, FeatureFlag, Toggle
# Register your models here.


admin.site.register(Project)
admin.site.register(FeatureFlag)
admin.site.register(Toggle)
