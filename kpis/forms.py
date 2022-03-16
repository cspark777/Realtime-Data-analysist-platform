from django import forms
from .models import KPI


class KPIForm(forms.ModelForm):

    category = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name', 'placeholder': 'Category'},
        ),
    )

    metric = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__description', 'placeholder': 'Name'},
        ),
    )

    indicator_type = forms.ChoiceField(
        required=True,
        widget=forms.Select(),
        choices=KPI.TYPE_CHOICES,
    )

    class Meta:
        model = KPI
        fields = (
            'category',
            'metric',
            'indicator_type',
        )
