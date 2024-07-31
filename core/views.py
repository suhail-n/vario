from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView


def index(request: HttpRequest) -> HttpResponse:
    active_project = request.COOKIES.get("active_project", None)
    if active_project:
        # redirect to the /projects/:name path
        return redirect("projects:detail", name=active_project)
    return redirect("projects:list")
