from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from account.models import Organisation


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SignUpForm, self).__init__(*args, **kwargs)
        company_id = self.request.session.get("company_id")
        if company_id:
            organisation = Organisation.objects.get(pk=company_id)
            self.fields['organisation__company_name'].initial = organisation.company_name
            self.fields['organisation__company_name'].disabled = True


    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'autocomplete': 'off'},
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'autocomplete': 'off'},
        ),
    )

    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs={'placeholder': 'E-mail', 'autocomplete': 'off'},
        ),
    )

    organisation__company_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(
            attrs={'placeholder': 'Company Name', 'autocomplete': 'off'},
        ),
    )

    password1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': '*********', 'autocomplete': 'off'},
        ),
    )

    password2 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': '*********', 'autocomplete': 'off'},
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
            'organisation__company_name',
            'password1',
            'password2',
        )


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs={'placeholder': 'E-mail', },
        ),
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'placeholder': 'Password', },
        ),
    )


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'First Name', 'autocomplete': 'off'},
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'Last Name', 'autocomplete': 'off'},
        ),
    )

    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'Company Name', 'autocomplete': 'off'},
        ),
    )

    role = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'styled-select'}),
        choices=get_user_model().ROLES,
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'company_name',
            'role',
        )
