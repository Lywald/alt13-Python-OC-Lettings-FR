"""Views for the site home page and error-page testing."""
from django.shortcuts import render


def index(request):
    """Render the site home page."""
    return render(request, 'index.html')


def trigger_500_error(request):
    """Raise an exception on purpose to exercise the custom 500 page."""
    raise Exception("Test 500")
