from django import forms
from .models import DataDictionary


class DataDictionaryForm(forms.ModelForm):

    name = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name required', 'placeholder': 'Data Dictionary Name'},
        ),
    )

    description = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Data Dictionary Description',
                   'class': 'new-item__description'},
        ),
    )

    items = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'hidden'},
        ),
    )

    class Meta:
        model = DataDictionary
        fields = (
            'name',
            'description',
        )
