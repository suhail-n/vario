import typing
from typing import Any
from typing import TypedDict
from typing import Unpack
from uuid import UUID

from django.db.models import Prefetch
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from environments.models import Environment
from feature_flags.forms import FeatureFlagCreateForm
from toggles.models import Toggle

from .forms import ProjectCreateForm
from .models import FeatureFlag
from .models import Project


# Create your views here.
class ProjectListView(ListView[Project]):
    model = Project
    # default template
    # template_name = "projects/projects_list.html"
    # template_name = "projects/project_list.html"
    # form_class = ProjectCreateForm
    context_object_name = "projects"

    # @typing.no_type_check
    # def get_context_data(self, **kwargs: Unpack[dict[str, Any]]) -> dict[str, Any]:
    #     context: dict[str, Any] = super().get_context_data(**kwargs)
    #     context["form"] = self.form_class()
    #     return context


class ProjectCreateView(CreateView[Project, ProjectCreateForm]):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("projects:list")

    # def form_valid(self, form):
    #     form.instance.user = (
    #         self.request.user
    #     )  # Assuming you want to assign the current user as the creator
    #     return super().form_valid(form)


class ProjectDetailView(DetailView[Project]):
    model = Project
    context_object_name = "project"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    queryset = Project.objects.prefetch_related(
        Prefetch(
            "featureflag_set",
            queryset=FeatureFlag.objects.prefetch_related(
                Prefetch(
                    "toggle_set",
                    queryset=Toggle.objects.prefetch_related(Prefetch("environment")),
                )
            ),
        ),
    )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project: Project = context["project"]
        # context["form"] = FeatureFlagCreateForm()

        class ProjectDetails(TypedDict):
            feature_flag: FeatureFlag
            toggles: list[Toggle]

        project_details: list[ProjectDetails] = []
        environments = Environment.objects.all()
        for feature_flag in project.featureflag_set.all():
            project_detail: ProjectDetails = {
                "feature_flag": feature_flag,
                "toggles": [],
            }
            # toggles = feature_flag.toggle_set.all()
            for env in environments:
                # we do this incase more environments are added in the future
                toggle, _ = Toggle.objects.get_or_create(
                    feature_flag=feature_flag, environment=env
                )
                project_detail["toggles"].append(toggle)
                # for toggle in toggles:
                #     if toggle.environment == env:
                #         project_detail["toggles"].append(toggle)
                #         break
            project_details.append(project_detail)
        context["project_details"] = project_details
        context["environments"] = environments
        return context


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
