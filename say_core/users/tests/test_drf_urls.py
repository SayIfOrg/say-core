from django.urls import resolve, reverse

from ..models import User


def test_user_detail(user: User):
    assert reverse("rest:user-detail", kwargs={"username": user.username}) == f"/api/users/{user.username}/"
    assert resolve(f"/api/users/{user.username}/").view_name == "rest:user-detail"


def test_user_list():
    assert reverse("rest:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "rest:user-list"


def test_user_me():
    assert reverse("rest:user-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "rest:user-me"
