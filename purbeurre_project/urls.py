"""purbeurre_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from .apps.pages import views as pages_views
from .apps.product import views as product_views
from .apps.users import views as password_view
from .apps.users import views as user_view
from .apps.users.views import PasswordsChangeView

urlpatterns = [
    path("", pages_views.home, name="home"),
    path("search/", product_views.SearchResultsView.as_view(), name="search"),
    path(
        "substitute/<int:product_id>",
        product_views.SubstituteResultsView.as_view(),
        name="substitute",
    ),
    path(
        "details/<int:pk>", product_views.ProductDetailsView.as_view(), name="details"
    ),
    path("save/", product_views.save_view, name="save"),
    path("favorites/", product_views.FavoritesView.as_view(), name="favorites"),
    path("delete/<int:pk>", product_views.DeleteView.as_view(), name="delete"),
    path("tos/", pages_views.tos, name="tos"),
    path("register/", user_view.register, name="register"),
    path("profile/", user_view.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password/",
        PasswordsChangeView.as_view(template_name="users/change-password.html"),
        name="password",
    ),
    path(
        "password_success",
        password_view.password_success,
        name="password_success",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
