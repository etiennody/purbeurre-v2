"""Processing profile in admin site page
"""
from django.contrib import admin

from .models import Profile

admin.site.register(Profile)
