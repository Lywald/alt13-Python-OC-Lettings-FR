"""Tests for the lettings app."""
import pytest
from django.urls import reverse

from lettings.models import Address, Letting


@pytest.fixture
def letting(db):
    """Create a letting with its address for use in tests."""
    address = Address.objects.create(
        number=1,
        street="Main Street",
        city="Springfield",
        state="IL",
        zip_code=62704,
        country_iso_code="USA",
    )
    return Letting.objects.create(title="Cozy flat", address=address)


def test_address_str(letting):
    """Address is displayed as its number and street."""
    assert str(letting.address) == "1 Main Street"


def test_letting_str(letting):
    """Letting is displayed as its title."""
    assert str(letting) == "Cozy flat"


def test_index_view(client, letting):
    """The index page returns 200 and lists the letting."""
    response = client.get(reverse("lettings:index"))
    assert response.status_code == 200
    assert b"Cozy flat" in response.content


def test_letting_view(client, letting):
    """The detail page returns 200 and shows the letting title."""
    response = client.get(reverse("lettings:letting", args=[letting.id]))
    assert response.status_code == 200
    assert b"Cozy flat" in response.content


# PIERRE
"""
@pytest.fixture
def letting(db):
    address = Address.objects.create(
        number=1,
        street="Main Street",
        city="Springfield",
        state="IL",
        zip_code=62704,
        country_iso_code="USA",
    )
    return Letting.objects.create(title="Cozy flat", address=address)


def test_address_str(letting):
    assert str(letting.address) == "1 Main Street


def test_letting_str(letting):
    assert str(letting) == "Cozy flat"


def test_index_view(client, letting):
    response = client.get(reverse("lettings:index))
    assert response.status_code == 200
    assert b"Cozy flat" in response.contnet


def test_letting_view(client, letting):
    response = client.get(reverse("lettings:letting"), args[letting.id]))
    assert response.status_code == 200
    assert b"Cozy flat" in response.content
"""
