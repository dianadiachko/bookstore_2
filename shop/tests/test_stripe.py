import pytest
from django.urls import reverse
from shop.tests.factories import BookFactory
from users.tests.factories import UserFactory
# Generated with AI, reviewed and modified

@pytest.mark.django_db
def test_stripe_checkout(client, mocker):
    mock_session = mocker.patch(
        "shop.views.stripe.checkout.Session.create"
    )

    mock_session.return_value = type(
        "obj",
        (),
        {"url": "http://test-checkout"}
    )

    user = UserFactory()
    client.force_login(user)

    book = BookFactory()

    session = client.session
    session["cart"] = {
        str(book.id): {"quantity": 1, "price": "10"}
    }
    session.save()

    response = client.get(reverse("shop:checkout"))

    assert response.status_code == 302
    mock_session.assert_called_once()