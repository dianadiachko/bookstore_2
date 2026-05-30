from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Book, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
import stripe
from django.conf import settings
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Order
from .cart import Cart
from django.http import JsonResponse
from .models import Book
from .models import Favorite
from django.http import JsonResponse


User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookListView(ListView):
    """
    Display list of books with search and filtering.

    Generated with AI, reviewed and modified.
    """
    model = Book
    template_name = "shop/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")

        if search:
            queryset = queryset.filter(title__icontains=search)

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class BookDetailView(DetailView):
    """
    Display book details.

    Generated with AI, reviewed and modified.
    """
    model = Book
    template_name = 'shop/book_detail.html'


class BookCreateView(CreateView):
    """
    Creates a new book entry.
    """
    model = Book
    template_name = 'shop/book_form.html'
    fields = '__all__'
    success_url = reverse_lazy('shop:list')


class BookUpdateView(UpdateView):
    """
    Updates an existing book.
    """
    model = Book
    template_name = 'shop/book_form.html'
    fields = '__all__'
    success_url = reverse_lazy('shop:list')


class BookDeleteView(DeleteView):
    """
    Deletes a book.
    """
    model = Book
    template_name = 'shop/book_confirm_delete.html'
    success_url = reverse_lazy('shop:list')


@permission_required('shop.can_publish_book')
def publish_book(request, pk):
    """
    Marks a book as available (published).

    Requires special permission.
    """
    book = get_object_or_404(Book, pk=pk)
    book.is_available = True
    book.save()
    return redirect('shop:list')


@login_required
def checkout(request):
    """
    Handle Stripe checkout.

    Generated with AI, reviewed and modified.
    """
    cart = Cart(request)

    items = list(cart)

    if not items:
        return HttpResponse("Cart is empty")

    line_items = []

    for item in items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item['book'].title,
                },
                "unit_amount": int(item['price'] * 100),
            },
            "quantity": item['quantity'],
        })

    line_items = []

    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item['book'].title,
                },
                "unit_amount": int(item['price'] * 100),
            },
            "quantity": item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost:8000/shop/success/",
        cancel_url="http://localhost:8000/shop/cancel/",
    )

    return redirect(session.url)


def success(request):
    """
    Handles successful payment.

    Creates order from cart and clears it.
    """
    cart = Cart(request)

    order = cart.create_order(
        user=request.user,
        email=request.user.email
    )

    return HttpResponse(f"Оплата успішна. Order #{order.id}")


def cancel(request):
    """
    Handles cancelled payment.
    """
    return HttpResponse("Оплата скасована")


@login_required
def add_favorite(request, pk):
    """
    Adds or removes a book from user's favorites.
    """
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    favorite, created = Favorite.objects.get_or_create(
        user=user,
        book=book
    )

    if not created:
        favorite.delete()

    return redirect('shop:detail', pk=pk)


@login_required
def my_orders(request):
    """
    Displays current user's orders.
    """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})


def cart_view(request):
    """
    Displays shopping cart contents.
    """
    cart = Cart(request)

    return render(request, 'shop/cart.html', {
        'items': list(cart),
        'total': cart.get_total_price()
    })


@login_required
def add_to_cart(request, pk):
    """
    Adds a book to the shopping cart.
    """
    cart = Cart(request)
    book = get_object_or_404(Book, pk=pk)

    cart.add(book=book, quantity=1)

    return redirect('shop:cart')


# список книг
async def async_books(request):
    """
    Return books asynchronously.

    Generated with AI, reviewed and modified.
    """
    books = [book async for book in Book.objects.all()]

    return JsonResponse({
        "books": [book.title for book in books]
    })


# деталі книги
async def async_book_detail(request, pk):
    """
    Async view returning book details.
    """
    book = await Book.objects.aget(pk=pk)

    return JsonResponse({
        "title": book.title
    })


#  створення книги
async def async_create_book(request):
    """
    Async view creating a book.
    """
    book = await Book.objects.acreate(
        title="Async Book"
    )

    return JsonResponse({
        "id": book.id
    })


def health(request):
    return JsonResponse({"status": "ok"})