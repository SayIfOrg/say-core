import pytest

from say_core.users.models import UserModel
from say_core.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> UserModel:
    return UserFactory()
