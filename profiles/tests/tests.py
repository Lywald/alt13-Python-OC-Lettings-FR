"""Tests for the profiles app."""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from profiles.models import Profile


@pytest.fixture
def profile(db):
    """Create a user and its profile for use in tests."""
    user = User.objects.create(username="bob")
    return Profile.objects.create(user=user, favorite_city="Paris")


def test_profile_str(profile):
    """Profile is displayed as its user's username."""
    assert str(profile) == "bob"


def test_index_view(client, profile):
    """The index page returns 200 and lists the profile."""
    response = client.get(reverse("profiles:index"))
    assert response.status_code == 200
    assert b"bob" in response.content


def test_profile_view(client, profile):
    """The detail page returns 200 and shows the username."""
    response = client.get(reverse("profiles:profile", args=["bob"]))
    assert response.status_code == 200
    assert b"bob" in response.content


# PIERRE
"""
@pytest.fixture
def profile(db):
    user = User.objects.create(username="bob")
    return Profile.objects.create(user=user, favorite_city="Paris")

def test_profile_str(profile):
    assert str(profile) == "bob"

def test_index_view(client, profile):
    response = client.get(reverse("profiles:index"))
    assert response.status_code == 200
    assert b"bob" in response.content

def test_profile_view(client, profile):
    response = client.get(reverse("profiles:profile", args=["bob"]))
    assert response.status_code == 200
    assert b"bob" in response.content
"""
