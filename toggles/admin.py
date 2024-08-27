from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Toggle


# Register your models here.
@admin.register(Toggle)
class ToggleAdmin(admin.ModelAdmin["Toggle"]):
    list_display = ("project_name", "feature_flag", "environment", "enabled")
    list_editable = ("enabled",)
    list_display_links = ("feature_flag", "project_name")
    search_fields = (
        "feature_flag__name",
        "environment__name",
        "feature_flag__project__name",
    )

    @admin.display(description="Project", ordering="feature_flag__project__name")
    def project_name(self, obj: Toggle) -> str:
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse(
                    "admin:projects_project_change", args=(obj.feature_flag.project.id,)
                ),
                obj.feature_flag.project.name,
            )
        )
