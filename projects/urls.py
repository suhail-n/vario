# urls file
from django.urls import URLPattern
from django.urls import path

from . import views


app_name: str = "projects"
urlpatterns: list[URLPattern] = [
    path("", views.list_projects, name="list"),
    path("details/<uuid:uuid>/", views.detail, name="detail"),
    path("create", views.create, name="create"),
    path(
        "api/internal/toggles/<int:toggle_id>",
        views.update_toggle,
        name="toggle",
    ),
]
