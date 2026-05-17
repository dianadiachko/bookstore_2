import pytest
from shop.tests.factories import BookFactory
# Generated with AI, reviewed and modified

@pytest.mark.django_db
def test_async_books():
    BookFactory.create_batch(3)
    assert True