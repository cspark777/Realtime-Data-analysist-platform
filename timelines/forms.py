from django import forms

from timelines.models import Timeline


class TimelineForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name required', 'minlength': '3', 'placeholder': 'Timeline Name'}
        ),
    )
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Timeline Description',
                   'class': 'new-item__description'},
        ),
    )

    class Meta:
        model = Timeline
        fields = [
            "name",
            "description"
        ]
