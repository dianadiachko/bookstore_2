import pytest
from shop.tests.factories import BookFactory
# Generated with AI, reviewed and modified

@pytest.mark.django_db
def test_book_create():
    book = BookFactory()

    assert book.id is not None
    assert book.title is not None