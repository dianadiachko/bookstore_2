from django.urls import path
from .views import checkout, success, cancel, my_orders
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    add_favorite,
    my_orders,
    checkout,
    success,
    cancel,
    cart_view,
    add_to_cart
)
from django.contrib import admin
from django.urls import path
from shop.views import health

app_name = "shop"

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('checkout/', checkout, name='checkout'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('<int:pk>/favorite/', add_favorite, name='favorite'),
    path('orders/', my_orders, name='my_orders'),
    path('cart/', cart_view, name='cart'),
    path('<int:pk>/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('admin/', admin.site.urls),
    path('health/', health),
]