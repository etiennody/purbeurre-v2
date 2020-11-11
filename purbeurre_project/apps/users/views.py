"""Users views
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import PasswordChangingForm, UserRegisterForm


def register(request):
    """Processing the register views

    Args:
        request (object): HttpRequest object

    Returns:
        objects: redirect register html document or login html document
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"{username} ! Votre compte a bien été créé. Vous pouvez "
                "maintenant vous y connecter !",
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    """Processing profile views

    Args:
        request (object): HttpRequest object

    Returns:
        object: a profile html document for users
    """
    return render(request, "users/profile.html")


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("password_success")


def password_success(request):
    return render(request, "users/password_success.html", {})
