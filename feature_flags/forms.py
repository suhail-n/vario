from django import forms
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from categories.models import get_default_category
from feature_flags.models import FeatureFlag
from projects.models import Project


class FeatureFlagCreateForm(forms.ModelForm[FeatureFlag]):
    # template_name = "form_templates/bootstrap_form.html"
    category: forms.ModelChoiceField[Category] = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=get_default_category,
        empty_label=_("Select a category"),
        required=True,
    )

    class Meta:
        model = FeatureFlag
        fields = ["name", "category", "description", "project"]

    def __init__(self, *args, **kwargs):
        self.project_uuid = kwargs.pop("project_uuid")
        super().__init__(*args, **kwargs)
        try:
            self.project = Project.objects.get(uuid=self.project_uuid)
            self.fields["project"].initial = self.project
            # add hidden input for project
            self.fields["project"].widget = forms.HiddenInput()
        except Project.DoesNotExist:
            # handle the case where the project does not exist
            raise forms.ValidationError(_("Project does not exist"))
        # set crispy form textbox row attribute
        self.fields["description"].widget.attrs["rows"] = 6
