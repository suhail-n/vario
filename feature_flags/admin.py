from django.contrib import admin

from feature_flags.models import FeatureFlag


# Register your models here.
admin.site.register(FeatureFlag)
