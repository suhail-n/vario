from typing import Any
from typing import cast
from uuid import UUID

from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from core import settings
from environments.models import Environment
from projects.models import Project
from toggles.models import Toggle

from .forms import FeatureFlagCreateForm
from .models import FeatureFlag


class FeatureFlagCreateView(CreateView[FeatureFlag, FeatureFlagCreateForm]):
    model = FeatureFlag
    form_class = FeatureFlagCreateForm
    project_uuid: UUID

    def get_success_url(self) -> str:
        return cast(
            str, reverse_lazy("projects:detail", kwargs={"uuid": self.project_uuid})
        )

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        """
        Dispatch is a method that is called by the view to dispatch
        the request to the correct handler method (e.g. get, post, etc.).
        It is a good place to capture URL kwargs.
        """
        try:
            uuid_val: UUID = cast(UUID, kwargs.get("project_uuid"))
            self.project_uuid = uuid_val
        except (TypeError, ValueError):
            return redirect("projects:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: FeatureFlagCreateForm) -> HttpResponse:
        try:
            project: Project = Project.objects.get(uuid=self.project_uuid)
        except Project.DoesNotExist:
            return redirect("projects:list")

        feature_flag: FeatureFlag = form.save(commit=False)

        feature_flag.project = project
        feature_flag.save()
        environments = Environment.objects.all()
        for environment in environments:
            Toggle.objects.create(feature_flag=feature_flag, environment=environment)
        self.request.session["SHOW_FORM_MODAL"] = False
        return super().form_valid(form)

    def form_invalid(self, form: FeatureFlagCreateForm) -> HttpResponse:
        for field in form:
            if field.errors:
                error = field.errors.as_text()
                messages.error(self.request, error)
            self.request.session["form_errors"] = form.errors

        return redirect("projects:detail", uuid=self.project_uuid)


@require_http_methods(["POST"])
@transaction.atomic
def feature_flag_create(request: HttpRequest, project_uuid: UUID) -> HttpResponse:
    try:
        project: Project = Project.objects.get(uuid=project_uuid)
    except Project.DoesNotExist:
        return redirect("projects:list")

    feature_flag_create_form = FeatureFlagCreateForm(request.POST)

    if feature_flag_create_form.is_valid():
        feature_flag: FeatureFlag = feature_flag_create_form.save(commit=False)
        feature_flag.project = project
        feature_flag.save()
        environments = Environment.objects.all()
        for environment in environments:
            feature_flag.toggle_set.create(
                feature_flag=feature_flag, environment=environment
            )

    return redirect("projects:detail", uuid=project_uuid)
