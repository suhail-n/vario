# urls file
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path

from . import views


app_name: str = "projects"
urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("create", views.ProjectCreateView.as_view(), name="create"),
    # path("create", views.ProjectListCreateView.as_view(), name="create"),
    path("details/<uuid:uuid>", views.ProjectDetailView.as_view(), name="detail"),
    path("<uuid:project_uuid>/featureflags/", include("feature_flags.urls")),
    # path("details/<uuid:uuid>/", views.detail, name="detail"),
    # path("<uuid:project_uuid>/featureflags/", include("feature_flags.urls")),
    # path("", views.ProjectListView.as_view(), name="list"),
    # path("", views.ProjectListCreateView.as_view(), name="list"),
]
