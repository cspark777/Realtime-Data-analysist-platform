from django import forms
from .models import Simulation


class SimulationForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name', 'placeholder': 'Name'}
        ),
    )

    description = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'new-item__description', 'cols': "", 'rows': "", "style": "height:100%", 'placeholder': 'Description'},
        ),
    )

    replicas = forms.IntegerField(
        initial=1,
        min_value=0,
        max_value=10,
        widget=forms.TextInput(
            attrs={'class': 'new-item__replicas', 'type': 'number', 'min': 1, 'max': 10, 'placeholder': 'Replicas'},
        ),
    )

    steps = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'hidden'},
        ),
    )

    type_event = forms.ChoiceField(
        required=False,
        widget=forms.Select(),
        choices=Simulation.EVENT_TYPES,
    )

    class Meta:
        model = Simulation
        fields = (
            'name',
            'description',
            'replicas',
            'type_event',
        )
