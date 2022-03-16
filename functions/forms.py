from django import forms

from .models import Function


class FunctionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Name', 'class': 'new-item__name required'},
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

    docker_image = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Docker Image Path', 'class': 'new-item__docker_image'},
        ),
    )

    class Meta:
        model = Function
        fields = (
            'name',
            'description',
            'docker_image',
        )
