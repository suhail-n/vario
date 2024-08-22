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
        toggles: list[Toggle]

    project_details: list[ProjectDetails] = []
    environments = Environment.objects.all()
    for feature_flag in project.featureflag_set.all():
        project_detail: ProjectDetails = {"feature_flag": feature_flag, "toggles": []}
        toggles = feature_flag.toggle_set.all()
        for env in environments:
            for toggle in toggles:
                if toggle.environment == env:
                    project_detail["toggles"].append(toggle)
                    break
        project_details.append(project_detail)

    return render(
        request,
        "projects/projects_detail.html",
        {
            "project": project,
            "project_details": project_details,
            "environments": environments,
        },
    )


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("projects:list")


def update_toggle(request: HttpRequest, toggle_id: int) -> HttpResponse:
    if request.method == "PUT":
        try:
            toggle = Toggle.objects.get(id=toggle_id)
            toggle.enabled = not toggle.enabled
            toggle.save()
            return HttpResponse(status=204)
        except Toggle.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=405)
