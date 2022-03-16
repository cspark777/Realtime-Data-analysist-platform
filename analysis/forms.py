from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name required', 'placeholder': 'Report Name'},
        ),
    )

    description = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Report Description',
                   'class': 'new-item__description'},
        ),
    )

    dsl = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'hidden'},
        ),
    )

    class Meta:
        model = Report
        fields = [
            "name",
            "description",
            "dsl",
        ]
