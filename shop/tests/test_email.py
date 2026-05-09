import pytest
from django.contrib.sessions.backends.db import SessionStore
from shop.tests.factories import BookFactory
from shop.cart import Cart


@pytest.mark.django_db
def test_order_sends_email(mocker, rf, user):
    mock_send = mocker.patch("django.core.mail.send_mail")

    book = BookFactory()

    request = rf.get("/")
    request.user = user

    request.session = SessionStore()
    request.session["cart"] = {
        str(book.id): {"quantity": 1, "price": "10"}
    }
    request.session.save()

    cart = Cart(request)
    cart.create_order(user=user, email=user.email)

    mock_send.assert_called_once()