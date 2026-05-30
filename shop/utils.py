from django.core.cache import cache
from .models import Book


def get_book_cached(book_id):
    key = f"book:{book_id}"

    book = cache.get(key)

    if not book:
        book = Book.objects.get(id=book_id)
        cache.set(key, book, 60 * 10)

    return book