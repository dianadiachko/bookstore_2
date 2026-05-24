import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from shop.tests.factories import BookFactory, UserFactory, CategoryFactory


@pytest.mark.django_db
def test_get_books_list():
    client = APIClient()
    BookFactory.create_batch(3)

    response = client.get("/api/books/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_get_single_book():
    client = APIClient()
    book = BookFactory()

    response = client.get(f"/api/books/{book.id}/")

    assert response.status_code == 200
    assert response.data["id"] == book.id


@pytest.mark.django_db
def test_create_book_admin():
    client = APIClient()
    user = UserFactory(is_staff=True)
    client.force_authenticate(user=user)

    category = CategoryFactory()

    response = client.post("/api/books/", {
        "title": "Test",
        "author": "Author",
        "price": 10,
        "stock": 5,
        "year": 2024,
        "genre": "Fiction",
        "category_id": 1
    })

    assert response.status_code in [200, 201]


@pytest.mark.django_db
def test_create_book_unauthorized():
    client = APIClient()

    response = client.post("/api/books/", {
        "title": "Test"
    })

    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_update_book():
    client = APIClient()
    user = UserFactory(is_staff=True)
    client.force_authenticate(user=user)

    book = BookFactory()

    response = client.patch(f"/api/books/{book.id}/", {
        "title": "Updated"
    })

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_book():
    client = APIClient()
    user = UserFactory(is_staff=True)
    client.force_authenticate(user=user)

    book = BookFactory()

    response = client.delete(f"/api/books/{book.id}/")

    assert response.status_code in [200, 204]

#categoruy

@pytest.mark.django_db
def test_get_categories():
    client = APIClient()
    CategoryFactory.create_batch(2)

    response = client.get("/api/categories/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category():
    client = APIClient()
    user = UserFactory(is_staff=True)
    client.force_authenticate(user=user)

    response = client.post("/api/categories/", {
        "name": "New",
        "slug": "new"
    })

    assert response.status_code in [200, 201]

#order

@pytest.mark.django_db
def test_get_orders_authenticated():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)

    response = client.get("/api/orders/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_orders_unauthenticated():
    client = APIClient()

    response = client.get("/api/orders/")

    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_jwt_token_obtain():
    client = APIClient()
    user = UserFactory(password="test123")

    response = client.post("/api/token/", {
        "username": user.username,
        "password": "test123"
    })

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_jwt_token_refresh():
    client = APIClient()
    user = UserFactory(password="test123")

    token = client.post("/api/token/", {
        "username": user.username,
        "password": "test123"
    }).data["refresh"]

    response = client.post("/api/token/refresh/", {
        "refresh": token
    })

    assert response.status_code == 200

#filter

@pytest.mark.django_db
def test_filter_books_by_category():
    client = APIClient()
    category = CategoryFactory()
    BookFactory(category=category)

    response = client.get(f"/api/books/?category={category.id}")

    assert response.status_code == 200


@pytest.mark.django_db
def test_pagination():
    client = APIClient()
    BookFactory.create_batch(25)

    response = client.get("/api/books/")

    assert response.status_code == 200
    assert len(response.data["results"]) <= 20

#throttling

@pytest.mark.django_db
def test_throttle():
    client = APIClient()
    BookFactory()

    for _ in range(105):
        response = client.get("/api/books/")

    assert response.status_code in [200, 429]



#permissions

@pytest.mark.django_db
def test_permission_denied_for_non_admin():
    client = APIClient()
    user = UserFactory(is_staff=False)
    client.force_authenticate(user=user)

    response = client.post("/api/books/", {
        "title": "Fail"
    })

    assert response.status_code in [403]

@pytest.mark.django_db
def test_book_search():
    client = APIClient()
    BookFactory(title="Python Book")

    response = client.get("/api/books/?search=Python")

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_price_filter():
    client = APIClient()
    BookFactory(price=50)

    response = client.get("/api/books/?price=50")

    assert response.status_code == 200


@pytest.mark.django_db
def test_empty_books():
    client = APIClient()

    response = client.get("/api/books/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_book():
    client = APIClient()

    response = client.get("/api/books/9999/")

    assert response.status_code in [404]


@pytest.mark.django_db
def test_order_requires_auth():
    client = APIClient()

    response = client.post("/api/orders/", {})

    assert response.status_code in [401, 403]