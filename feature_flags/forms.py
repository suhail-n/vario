from django import forms
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from categories.models import get_default_category
from feature_flags.models import FeatureFlag


class FeatureFlagCreateForm(forms.ModelForm[FeatureFlag]):
    template_name = "form_templates/bootstrap_form.html"
    category: forms.ModelChoiceField[Category] = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=get_default_category,
        empty_label=_("Select a category"),
        required=True,
    )

    class Meta:
        model = FeatureFlag
        fields = ["name", "category", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all Category instances
        categories = Category.objects.all()

        # Create a dictionary mapping object IDs to friendly names
        choices = [(str(cat.id), cat.get_name_display()) for cat in categories]

        # Set the choices for the category field
        self.fields["category"].choices = choices

        # Set the widget to a Select widget
        self.fields["category"].widget = forms.Select()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            old_form_data = self.request.session["form_errors"]
            context["form"] = self.form_class(old_form_data)
        except:
            context["form"] = self.form_class()
        return context
