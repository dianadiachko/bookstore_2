from rest_framework import viewsets, permissions
from .models import Book, Category, Order
from .serializers import BookSerializer, CategorySerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ["category", "price"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return []


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]


@method_decorator(cache_page(60 * 5))
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)