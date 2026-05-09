import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
django.setup()

from shop.models import Book, Category
from django.db.models import Count, Q, Sum

def test_queries():
    cheap_books = Book.objects.filter(price__lt=500)
    print("Дешеві книги:")
    for b in cheap_books:
        print(f"{b.title} - {b.price}")

    categories = Category.objects.annotate(num_books=Count('books'))  # <- 'books', бо related_name
    print("\nКількість книг по категоріях:")
    for c in categories:
        print(f"{c.name}: {c.num_books}")

    books_or = Book.objects.filter(Q(author="T. Shevchenko") | Q(price__lt=300))
    print("\nКниги T. Shevchenko або дешевші за 300:")
    for b in books_or:
        print(f"{b.title} - {b.author} - {b.price}")

    total_price = Book.objects.aggregate(total=Sum('price'))
    print("\nЗагальна сума всіх книг:", total_price['total'])

if __name__ == "__main__":
    test_queries()