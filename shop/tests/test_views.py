import pytest
from django.urls import reverse
from shop.tests.factories import BookFactory
# Generated with AI, reviewed and modified

@pytest.mark.django_db
def test_books_view(client):
    BookFactory()
    url = reverse("shop:list")
    response = client.get(url)

    assert response.status_code == 200