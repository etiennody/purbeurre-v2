"""Users model
"""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Profile model

    Args:
        models (subclass): a python class that subclasses django.db.models.Model

    Returns:
        string: account of the user profile
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"Compte de {self.user.username}"
