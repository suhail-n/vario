from typing import TypedDict
from uuid import UUID

from django.db.models import Prefetch
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from environments.models import Environment

from .forms import ProjectCreateForm
from .models import FeatureFlag
from .models import Project
from .models import Toggle


# Create your views here.


def list_projects(request: HttpRequest) -> HttpResponse:
    projects = Project.objects.all()
    form = ProjectCreateForm()
    return render(
        request,
        "projects/projects_list.html",
        context={"projects": projects, "form": form},
    )


def detail(request: HttpRequest, uuid: UUID) -> HttpResponse:
    try:
        project: Project = Project.objects.prefetch_related(
            Prefetch(
                "featureflag_set",
                queryset=FeatureFlag.objects.prefetch_related(
                    Prefetch(
                        "toggle_set",
                        queryset=Toggle.objects.prefetch_related(
                            Prefetch("environment")
                        ),
                    )
                ),
            ),
        ).get(uuid=uuid)
    except Project.DoesNotExist:
        return redirect("projects:list")

    class ProjectDetails(TypedDict):
        feature_flag: FeatureFlag
        toggle: Toggle
        environment: Environment

    project_details: list[ProjectDetails] = []
    for feature_flag in project.featureflag_set.all():
        for toggle in feature_flag.toggle_set.all():
            project_details.append(
                {
                    "feature_flag": feature_flag,
                    "toggle": toggle,
                    "environment": toggle.environment,
                }
            )

    return render(
        request,
        "projects/projects_detail.html",
        {"project": project, "project_details": project_details},
    )


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("projects:list")
