# urls file
from django.urls import URLPattern
from django.urls import path

from . import views


app_name: str = "toggles"
urlpatterns: list[URLPattern] = [
    path(
        "api/internal/toggles/<int:toggle_id>",
        views.update_toggle,
        name="toggle",
    ),
]
