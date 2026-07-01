"""Views for listing profiles and displaying profile details."""
from django.shortcuts import render

from .models import Profile


def index(request):
    """Render the list of all profiles."""
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """Render the details of a single profile identified by its username."""
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
