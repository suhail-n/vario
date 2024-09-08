from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from projects.models import Project


class ProjectCreateForm(forms.ModelForm[Project]):
    class Meta:
        model = Project
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # description placeholder
        self.fields["description"].widget.attrs["placeholder"] = "..."
        self.fields["description"].widget.attrs["rows"] = 6
