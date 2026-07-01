"""Admin registration for the profiles models."""
from django.contrib import admin

from .models import Profile

admin.site.register(Profile)
