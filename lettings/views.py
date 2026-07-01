"""Views for listing lettings and displaying letting details."""
from django.shortcuts import render

from .models import Letting


def index(request):
    """Render the list of all lettings."""
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """Render the details of a single letting identified by its id."""
    letting = Letting.objects.get(id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
