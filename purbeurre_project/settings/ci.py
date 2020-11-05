from .base import *

SECRET_KEY = "x5`4/@wh!=ZRu%&fcA{lrSaV"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}