"""Users apps
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users configuration app named users

    Args:
        AppConfig (subclass): instance for users installed application
    """
    name = "users"

    def ready(self):
        import users.signals
