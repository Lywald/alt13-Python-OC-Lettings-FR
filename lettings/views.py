"""Views for listing lettings and displaying letting details."""
import logging

from django.shortcuts import render

from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """Render the list of all lettings."""
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """Render the details of a single letting identified by its id."""
    logger.info("Fetching letting id=%s and its address", letting_id)
    try:
        letting = Letting.objects.get(id=letting_id)
    except Letting.DoesNotExist:
        # ERROR level -> sent to Sentry as an event.
        logger.error("Letting id=%s does not exist", letting_id)
        raise

    address = letting.address
    logger.info("Serving letting '%s' at address '%s'", letting.title, address)
    context = {
        'title': letting.title,
        'address': address,
    }
    return render(request, 'lettings/letting.html', context)
