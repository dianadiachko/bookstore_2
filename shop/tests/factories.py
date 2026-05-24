import factory
from shop.models import Book, Category
from django.contrib.auth import get_user_model

# Generated with AI, reviewed and modified

User = get_user_model()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category-{n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "test123")
    is_staff = False


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    category = factory.SubFactory(CategoryFactory)

    title = factory.Faker("sentence")
    author = factory.Faker("name")
    price = 10  # важливо
    description = factory.Faker("text")
    stock = 10
    year = 2024
    genre = "Fiction"
    is_available = True