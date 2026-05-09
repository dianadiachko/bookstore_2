import pytest
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_create():
    user = UserFactory()

    assert user.username is not None
    assert user.id is not None