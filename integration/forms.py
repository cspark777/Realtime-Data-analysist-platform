from django import forms

from .models import DataSource
from streams.models import Stream


class DataSourceForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Name', 'class': 'new-item__name required' },
        ),
    )

    description = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Description', 'class': 'new-item__description',
                   'style': 'height: 40px;'},
        ),
    )
    stream = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Stream.objects.all(),
        empty_label=None,
    )
    source_type = forms.ChoiceField(
        widget=forms.Select(),
        choices=DataSource.SOURCE_TYPES,
    )

    class Meta:
        model = DataSource
        fields = (
            'name',
            'description',
            'source_type',
            'stream'
        )
