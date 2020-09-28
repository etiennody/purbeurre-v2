"""Users forms for registration and authentication
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """Custom register form with email field

    Args:
        UserCreationForm (class): A form that creates a user, with
        no privileges, from the given username and password.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    """processing authentication form with inactive users

    Args:
        AuthenticationForm (class): Base class for authenticating users. Extend
        this to get a form that accepts username/password logins.
    """

    def confirm_login_allowed(self, user):
        pass
