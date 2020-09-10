"""Users App views tests
"""
import time
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
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
        """Valid if status code for register page is success"""
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_valid_register_view(self):
        """Valid if register page use the right template"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_valid_user_exists_after_registration(self):
        """Valid if Alice Dupond is in db after registration"""
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
    """Register functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver", chrome_options=chrome_options
        )

    def test_valid_live_register_page(self):
        """Validate data entries on the registration page"""
        self.driver.get("http://127.0.0.1:8000/register/")
        print(self.driver.title)
        username = self.driver.find_element_by_id("id_username")
        first_name = self.driver.find_element_by_id("id_first_name")
        last_name = self.driver.find_element_by_id("id_last_name")
        email = self.driver.find_element_by_id("id_email")
        password1 = self.driver.find_element_by_id("id_password1")
        password2 = self.driver.find_element_by_id("id_password2")
        submit = self.driver.find_element_by_class_name("btn")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        username.send_keys("BobRobert")
        first_name.send_keys("Bob")
        last_name.send_keys("Robert")
        email.send_keys("bobrobert@test.com")
        password1.send_keys("fglZfYmr%?,")
        password2.send_keys("fglZfYmr%?,")
        submit.click()

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000/register")
        self.assertIn("Vous avez déjà un compte ?", self.driver.page_source)
        self.assertTrue(User.objects.filter(username="BobRobert").exists())

    def tearDown(self):
        self.driver.close()


class LoginTests(TestCase):
    """Login Unit Test"""

    def setUp(self):
        """Login test set up"""
        self.credentials = {"username": "BobRobert", "password": "fglZfYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_login_page(self):
        """Valid if status code for login page is success"""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_valid_login_page_view(self):
        """Valid if login page use the right template"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_valid_user_login(self):
        """Valid if user can be authenticated"""
        response = self.client.post(reverse("login"), self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_invalid_user_login(self):
        """Unvalid user login if user doesn't exist in db"""
        response = self.client.post(
            reverse("login"),
            {"username": "AliceRobert", "password": "fglZfYmr"},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_valid_display_hommepage_after_valid_login(self):
        """Valid homepage template after user is logged"""
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.client.post(reverse("login"), self.credentials, follow=True)
        self.assertTemplateUsed("pages/home.html")


class LoginSeleniumTest(unittest.TestCase):
    """Login functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

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
        """Validate data entries on the login page"""
        self.driver.get("http://127.0.0.1:8000/login/")
        print(self.driver.title)
        username = self.driver.find_element_by_id("id_username")
        password = self.driver.find_element_by_id("id_password")
        submit = self.driver.find_element_by_id("submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,")
        submit.send_keys(Keys.RETURN)

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000")
        self.assertIn("Accueil :: Purbeurre", self.driver.title)

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
        """Valid if status code for profile page is success"""
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

    def test_valid_profil_page_view(self):
        """Valid if register page use the right template"""
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
