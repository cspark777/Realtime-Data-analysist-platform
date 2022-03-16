from django import forms

from streams.models import Stream
from schemas.models import Schema


class StreamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StreamForm, self).__init__(*args, **kwargs)
        project_id = self.initial.get('project_id')
        if project_id:
            self.fields.get('schema').queryset = Schema.objects.filter(
                schemafield__isnull=False, project_id=project_id).distinct()

    display_name = forms.CharField(
        label='Name',
        max_length=200,
        min_length=3,
        widget=forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'Stream Name', 'class': 'new-item__name'}
        ),
    )

    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={'cols': "", 'rows': "", 'placeholder': 'Stream Description',
                   'class': 'new-item__description'},
        ),
    )

    schema = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Schema.objects.none(),
        empty_label='Choose Event Definition',
    )

    retention_period = forms.CharField(
        label='Retention Period',
        widget=forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'Retention Period', 'class': 'new-item__run-type'}
        ),
        initial='1 Year',
    )

    is_countable = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={}),
        initial=True
    )

    share = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={}),
        initial=False
    )

    class Meta:
        model = Stream
        fields = [
            "display_name",
            "description",
            "schema",
            "retention_period",
            "is_countable",
            "share"
        ]
