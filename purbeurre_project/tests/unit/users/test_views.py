"""Users App views tests"""
import time
import unittest

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


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
        self.assertEqual(response.status_code, 200)

    def test_valid_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="AliceDupond").exists())


class RegisterSeleniumTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver", chrome_options=chrome_options
        )

    def test_valid_live_register_page(self):
        username = "BobRobert"
        first_name = "Bob"
        last_name = "Robert"
        email = "bobrobert@test.com"
        password1 = "fglZfYmr%?,"
        password2 = "fglZfYmr%?,"
        self.driver.get("http://127.0.0.1:8000/register/")
        print(self.driver.title)
        element = self.driver.find_element_by_id("id_username")
        element = self.driver.find_element_by_id("id_first_name")
        element = self.driver.find_element_by_id("id_last_name")
        element = self.driver.find_element_by_id("id_email")
        element = self.driver.find_element_by_id("id_password1")
        element = self.driver.find_element_by_id("id_password2")
        submit = self.driver.find_element_by_class_name("btn")
        element.send_keys(username)
        element.send_keys(first_name)
        element.send_keys(last_name)
        element.send_keys(email)
        element.send_keys(password1)
        element.send_keys(password2)
        submit.click()

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000/register")
        self.assertIn("Tu as déjà un compte ?", self.driver.page_source)

    def tearDown(self):
        self.driver.close()


class LoginTests(TestCase):
    """Login Unit Test"""

    def setUp(self):
        """Login test set up"""
        self.credentials = {"username": "BobRobert", "password": "fglZfYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_login_page(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_valid_login_page_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
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


class LoginSeleniumTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver", chrome_options=chrome_options
        )
        user = User.objects.create(
            username="BobRobert",
            first_name="Bob",
            last_name="Robert",
            email="test_bob@test.com",
        )
        user.set_password("fglZfYmr%?,")
        user.save()
        super(LoginSeleniumTest, self).setUp()

    def test_valid_live_login_page(self):
        username = "BobRobert"
        password = "fglZfYmr%?,"
        self.driver.get("http://127.0.0.1:8000/login/")
        print(self.driver.title)
        element = self.driver.find_element_by_id("id_username")
        element = self.driver.find_element_by_id("id_password")
        submit = self.driver.find_element_by_id("submit-button")
        element.send_keys(username)
        element.send_keys(password)
        submit.send_keys(Keys.RETURN)

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000/login")
        self.assertIn("Besoin d'un compte ?", self.driver.page_source)

    def tearDown(self):
        self.driver.close()
        super(LoginSeleniumTest, self).tearDown()


class LogoutTests(TestCase):
    """Logout Unit Test"""

    def setUp(self):
        """Logout test setup"""
        self.credentials = {"username": "BobRobert", "password": "fglZ9fYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_logout_page(self):
        """Test logout view using verbal url"""
        response = self.client.get("logout/")
        self.assertEqual(response.status_code, 404)

    def test_valid_logout_page_view(self):
        """Test logout view using reverse url"""
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 200)

    def test_valid_profil_page_view(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
