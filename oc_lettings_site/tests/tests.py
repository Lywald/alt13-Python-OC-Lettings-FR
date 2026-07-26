"""Tests for the oc_lettings_site project."""
import pytest
from django.urls import reverse

from lettings.models import Address, Letting


def test_index_view(client):
    """The home page returns 200."""
    response = client.get(reverse("index"))
    assert response.status_code == 200


def test_trigger_500_error(client):
    """The debug route raises an exception on purpose."""
    with pytest.raises(Exception, match="Test 500"):
        client.get("/trigger-500-error/")


def test_navigate_home_to_letting_detail(client, db):
    """Integration: follow home -> lettings list -> letting detail across apps.

    Exercises the full stack together: root URLconf, the included lettings URLs,
    both views, the Letting->Address ORM join and two templates.
    """
    address = Address.objects.create(
        number=7, street="Main Street", city="Springfield",
        state="IL", zip_code=62704, country_iso_code="USA",
    )
    letting = Letting.objects.create(title="Cozy flat", address=address)

    # 1. Home page is reachable.
    assert client.get(reverse("index")).status_code == 200

    # 2. The lettings list shows the letting and links to its detail page.
    index = client.get(reverse("lettings:index"))
    assert index.status_code == 200
    assert b"Cozy flat" in index.content
    detail_url = reverse("lettings:letting", args=[letting.id])
    assert detail_url.encode() in index.content

    # 3. Following that link renders the title and the joined address.
    detail = client.get(detail_url)
    assert detail.status_code == 200
    assert b"Cozy flat" in detail.content
    assert b"Main Street" in detail.content


# PIERRE
"""
def test_index_view(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200

def test_trigger_500_error(client):
    with pytest.raises(Exception, match="Test 500"):
        client.get("/trigger-500-error/")
"""
