from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect


def index(request: HttpRequest) -> HttpResponse:
    active_project = request.COOKIES.get("active_project", None)
    if active_project:
        # redirect to the /projects/:name path
        return redirect("projects:detail", name=active_project)
    return redirect("projects:list")
