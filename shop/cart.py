from decimal import Decimal
from django.conf import settings
from .models import Book, Order, OrderItem, Favorite
from django.db import transaction
from django.core.mail import send_mail


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart
        self.request = request

    def add(self, book, quantity=1, override_quantity=False):
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {
                'quantity': 0,
                'price': str(book.price)
            }

        if override_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        for book in books:
            self.cart[str(book.id)]['book'] = book

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def create_order(self, user, email):
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                email=email
            )

            for item in self:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            self.clear()

        send_mail(
            'Замовлення створено',
            f'Ваше замовлення #{order.id} успішно створено.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return order

    # додати у обраного️
    def add_to_favorite(self, user, book):
        Favorite.objects.get_or_create(
            user=user,
            book=book
        )

    def remove_from_favorite(self, user, book):
        Favorite.objects.filter(
            user=user,
            book=book
        ).delete()