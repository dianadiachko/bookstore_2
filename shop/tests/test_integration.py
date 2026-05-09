import pytest
from django.urls import reverse
from shop.tests.factories import BookFactory


@pytest.mark.django_db
def test_user_flow_add_to_cart(client, user):
    client.force_login(user)

    book = BookFactory()

    response = client.get(
        reverse("shop:add_to_cart", args=[book.id])
    )

    assert response.status_code == 302

@pytest.mark.django_db
def test_user_flow_checkout(client, mocker, user):
    client.force_login(user)

    mocker.patch(
        "shop.views.stripe.checkout.Session.create",
        return_value=type("obj", (), {"url": "/ok"})
    )

    book = BookFactory()

    session = client.session
    session["cart"] = {
        str(book.id): {"quantity": 1, "price": "10"}
    }
    session.save()

    response = client.get(reverse("shop:checkout"))

    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_user_flow_cart_view(client, user):
    client.force_login(user)

    response = client.get(reverse("shop:cart"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_flow_orders(client, user):
    client.force_login(user)

    response = client.get(reverse("shop:my_orders"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_flow_favorite(client, user):
    client.force_login(user)

    book = BookFactory()

    response = client.get(
        reverse("shop:favorite", args=[book.id])
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_user_flow_book_list(client):
    BookFactory.create_batch(3)

    response = client.get(reverse("shop:list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_flow_book_detail(client):
    book = BookFactory()

    response = client.get(
        reverse("shop:detail", args=[book.id])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_flow_success(client, user):
    client.force_login(user)

    response = client.get(reverse("shop:success"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_flow_cancel(client):
    response = client.get(reverse("shop:cancel"))

    assert response.status_code == 200

@pytest.mark.django_db
def test_user_flow_checkout_page(client, mocker, user):
    client.force_login(user)

    mocker.patch(
        "shop.views.stripe.checkout.Session.create",
        return_value=type("obj", (), {"url": "/ok"})
    )

    response = client.get(reverse("shop:checkout"))

    assert response.status_code in [200, 302]