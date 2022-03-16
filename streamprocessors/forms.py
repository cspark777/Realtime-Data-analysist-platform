from django import forms

from .models import StreamProcessor
from .models import TestSimulate


class StreamProcessorForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name required', 'placeholder': 'Stream Processor Name'}
        ),
    )
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={'cols': "", 'rows': "", 'placeholder': 'Stream Processor Description',
                   'class': 'new-item__description'},
        ),
    )
    replicas = forms.IntegerField(
        initial=1,
        max_value=10,
        widget=forms.TextInput(
            attrs={'class': 'new-item__replicas required', 'type': 'number', 'min': 1, 'max': 10, 'placeholder': 'Replicas'},
        ),
    )

    steps = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'hidden'},
        ),
    )

    additional_integrity_checks = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Additional Integrity Checks',
        initial=False,
    )

    class Meta:
        model = StreamProcessor
        fields = [
            "name",
            "description",
            "replicas",
            "additional_integrity_checks",
        ]


class TestSimulateForm(forms.Form):
    event = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
    )
    stream = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
    )

    class Meta:
        model = TestSimulate
        fields = (
            'event',
            'stream',
        )
