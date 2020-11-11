"""Users forms for registration and authentication
"""
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
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


class PasswordChangingForm(PasswordChangeForm):
    """Custom changing password form

    Args:
        PasswordChangeForm (class): A form that lets a user change their password by entering their old password.
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label="Ancien mot de passe",
    )
    new_password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label="Nouveau mot de passe",
    )
    new_password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label="Confirmation du nouveau mot de passe",
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")
