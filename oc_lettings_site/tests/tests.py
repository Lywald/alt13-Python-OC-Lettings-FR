"""Tests for the oc_lettings_site project."""
import pytest
from django.urls import reverse


def test_index_view(client):
    """The home page returns 200."""
    response = client.get(reverse("index"))
    assert response.status_code == 200


def test_trigger_500_error(client):
    """The debug route raises an exception on purpose."""
    with pytest.raises(Exception, match="Test 500"):
        client.get("/trigger-500-error/")


# PIERRE
"""
def test_index_view(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200

def test_trigger_500_error(client):
    with pytest.raises(Exception, match="Test 500"):
        client.get("/trigger-500-error/")
"""
