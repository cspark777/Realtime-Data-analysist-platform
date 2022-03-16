from django import forms

from .models import Search


class SearchForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new-item__name required', 'placeholder': 'Search Name'},
        ),
    )

    description = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search Description',
                   'class': 'new-item__description'},
        ),
    )

    stream = forms.CharField(
        widget=forms.Select()
    )

    class Meta:
        model = Search
        fields = [
            "name",
            "description",
            "stream",
            "time_window",
            "search_data"
        ]
