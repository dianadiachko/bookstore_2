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



User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookListView(ListView):
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
    model = Book
    template_name = 'shop/book_detail.html'


class BookCreateView(CreateView):
    model = Book
    template_name = 'shop/book_form.html'
    fields = '__all__'
    success_url = reverse_lazy('shop:list')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'shop/book_form.html'
    fields = '__all__'
    success_url = reverse_lazy('shop:list')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'shop/book_confirm_delete.html'
    success_url = reverse_lazy('shop:list')


@permission_required('shop.can_publish_book')
def publish_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_available = True
    book.save()
    return redirect('shop:list')


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return HttpResponse("Cart is empty")

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
    cart = Cart(request)

    order = cart.create_order(
        user=request.user,
        email=request.user.email
    )

    return HttpResponse(f"Оплата успішна. Order #{order.id}")


def cancel(request):
    return HttpResponse("Оплата скасована")


@login_required
def add_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if book in user.favorites.all():
        user.favorites.remove(book)
    else:
        user.favorites.add(book)

    return redirect('shop:detail', pk=pk)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})


def cart_view(request):
    cart = Cart(request)

    return render(request, 'shop/cart.html', {
        'items': list(cart),
        'total': cart.get_total_price()
    })


@login_required
def add_to_cart(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, pk=pk)

    cart.add(book=book, quantity=1)

    return redirect('shop:cart')