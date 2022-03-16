from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Name', },
        ),
    )

    description = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Description', },
        ),
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
        )
