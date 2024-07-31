from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectCreateForm

# Create your views here.


def list(request: HttpRequest) -> HttpResponse:
    projects = Project.objects.all()
    form = ProjectCreateForm()
    return render(request, "projects/projects_list.html", context={"projects": projects, "form": form})


def detail(request: HttpRequest, uuid: UUID) -> HttpResponse:
    project: Project
    try:
        project = Project.objects.get(uuid=uuid)
    except Project.DoesNotExist:
        return redirect("projects:list")

    return render(request, "projects/projects_detail.html", {"project": project})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("projects:list")
