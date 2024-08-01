from django import forms

from projects.models import Project


class ProjectCreateForm(forms.ModelForm):
    template_name = "form_templates/bootstrap_form.html"

    class Meta:
        model = Project
        fields = ["name"]
