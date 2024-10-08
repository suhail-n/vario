# urls file
from django.urls import URLPattern
from django.urls import path

from . import views


app_name: str = "feature_flags"
urlpatterns: list[URLPattern] = [
    path(
        "create",
        views.FeatureFlagCreateView.as_view(),
        name="create",
    ),
]
