"""Users App views tests"""
import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegisterForm
from users.models import Profile


class RegisterTests(TestCase):
    """Register Unit Test"""

    def setUp(self):
        """Register test set up"""
        self.credentials = {
            "username": "BobRobert",
            "first_name": "Bob",
            "last_name": "Robert",
            "email": "test_bob@test.com",
            "password": "fglZfYmr%?,",
        }

    def test_valid_register_page(self):
        response = self.client.get("/register/")
        self.assertEquals(response.status_code, 200)

    def test_valid_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_valid_user_exists_after_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "AliceDupond",
                "email": "test_alice@test.com",
                "password1": "dhjO0iZxt}!;",
                "password2": "dhjO0iZxt}!;",
                "robot": True,
            },
            follow=True,
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="AliceDupond").exists())


class LoginTests(TestCase):
    """Login Unit Test"""

    def setUp(self):
        """Login test set up"""
        self.credentials = {"username": "BobRobert", "password": "fglZfYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_login_page(self):
        response = self.client.get("/login/")
        self.assertEquals(response.status_code, 200)

    def test_valid_login_page_view(self):
        response = self.client.get(reverse("login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_valid_user_login(self):
        response = self.client.post(reverse("login"), self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_invalid_user_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "AliceRobert", "password": "fglZfYmr"},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_valid_display_hommepage_after_valid_login(self):
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.client.post(reverse("login"), self.credentials, follow=True)
        self.assertTemplateUsed("pages/home.html")


class LogoutTests(TestCase):
    """Logout Unit Test"""

    def setUp(self):
        """Logout test setup"""
        self.credentials = {"username": "BobRobert", "password": "fglZ9fYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_logout_page(self):
        """Test logout view using verbal url"""
        response = self.client.get("logout/")
        self.assertEquals(response.status_code, 404)

    def test_valid_logout_page_view(self):
        """Test logout view using reverse url"""
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        response = self.client.get(reverse("logout"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/logout.html")


class ProfileTests(TestCase):
    """Profile Unit Test"""

    def setUp(self):
        """Profile test set up"""
        self.credentials = {
            "username": "BobRobert",
            "email": "test_bob@test.f",
            "password": "fglZ9fYmr%?,",
        }
        User.objects.create_user(
            username="AliceDupond",
            email="test_alice@test.com",
            password="dhjO0iZxt}!;",
        )
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_valid_profile_page(self):
        response = self.client.get("/profile/")
        self.assertEquals(response.status_code, 200)

    def test_valid_profil_page_view(self):  # pragma: no cover
        response = self.client.get(reverse("profile"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
