"""Database model for user profiles."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """A user profile extending the built-in User with a favorite city."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the associated user's username."""
        return self.user.username
