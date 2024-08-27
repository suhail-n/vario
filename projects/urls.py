# urls file
from django.urls import URLPattern
from django.urls import path

from . import views


app_name: str = "projects"
urlpatterns: list[URLPattern] = [
    path("create", views.ProjectCreateView.as_view(), name="create"),
    path("details/<uuid:uuid>/", views.ProjectDetailView.as_view(), name="detail"),
    # path("details/<uuid:uuid>/", views.detail, name="detail"),
    path("", views.ProjectListView.as_view(), name="list"),
]
