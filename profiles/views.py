"""Views for listing profiles and displaying profile details."""
import logging

from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """Render the list of all profiles."""
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """Render the details of a single profile identified by its username."""
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        logger.error("Profile %s does not exist", username)
        raise
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
