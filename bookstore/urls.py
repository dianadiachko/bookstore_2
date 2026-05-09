from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from shop.views import (
    async_books,
    async_book_detail,
    async_create_book
)

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),

    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('user/', include('users.urls')),
    path('shop/', include('shop.urls')),

    # async API
    path('async/books/', async_books),
    path('async/books/<int:pk>/', async_book_detail),
    path('async/books/create/', async_create_book),
]