import factory
from shop.models import Book, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    category = factory.SubFactory(CategoryFactory)

    title = factory.Faker("sentence")
    author = factory.Faker("name")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)

    description = factory.Faker("text")

    stock = 10
    year = 2024
    genre = "Fiction"
    is_available = True