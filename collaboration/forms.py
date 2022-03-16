from django import forms
from django.contrib.auth import get_user_model
from .models import Collaboration
from projects.models import Project
from django.core.exceptions import NON_FIELD_ERRORS


class CollaborationForm(forms.ModelForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'placeholder': 'E-mail', 'autocomplete': 'off'},
        ),
    )

    class Meta:
        model = Collaboration
        fields = [
            'email',
            'access_type',
        ]
