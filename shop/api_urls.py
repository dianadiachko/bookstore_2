from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet, CategoryViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = router.urls