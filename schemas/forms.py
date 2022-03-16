from django import forms

from .models import Schema


class SchemaForm(forms.ModelForm):
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
    file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'hidden': True}))
    class Meta:
        model = Schema
        fields = (
            'name',
            'description',
        )
