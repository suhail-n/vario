# urls file
from django.urls import URLPattern
from django.urls import path

from . import views


app_name: str = "categories"
urlpatterns: list[URLPattern] = [
    path("", views.ListCategories.as_view(), name="list"),
]
