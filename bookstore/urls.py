from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('admin/', admin.site.urls),
]

# debug toolbarf
if settings.DEBUG:
    pass

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('users.urls')),
    path('shop/', include('shop.urls')),
]