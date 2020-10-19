"""Functional tests for users app
"""
import time
import unittest

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class RegisterSeleniumTest(LiveServerTestCase):
    """Register functional test with selenium

    Args:
        LiveServerTestCase ([type]): Do basically the same as TransactionTestCase but also launch a live HTTP server in a separate thread so that the tests use another testing framework, as Selenium, instead of the built-in dummy client.
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def test_valid_live_register_page(self):
        """Validate data entries on the registration page"""
        self.driver.get("%s%s" % (self.live_server_url, "/register/"))
        print(self.driver.title)
        username = self.driver.find_element(By.ID, "id_username")
        first_name = self.driver.find_element(By.ID, "id_first_name")
        last_name = self.driver.find_element(By.ID, "id_last_name")
        email = self.driver.find_element(By.ID, "id_email")
        password1 = self.driver.find_element(By.ID, "id_password1")
        password2 = self.driver.find_element(By.ID, "id_password2")
        submit = self.driver.find_element(By.CLASS_NAME, "btn")
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
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/login"))
        self.assertIn("Se connecter", self.driver.page_source)
        self.assertTrue(User.objects.filter(username="BobRobert").exists())

    def tearDown(self):
        self.driver.close()


class LoginSeleniumTest(LiveServerTestCase):
    """Login functional test with selenium

    Args:
        LiveServerTestCase ([type]): Do basically the same as TransactionTestCase but also launch a live HTTP server in a separate thread so that the tests use another testing framework, as Selenium, instead of the built-in dummy client.
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
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
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        print(self.driver.title)
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,")
        submit.send_keys(Keys.RETURN)

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s" % (self.live_server_url))
        self.assertIn("Accueil :: Purbeurre", self.driver.title)

    def tearDown(self):
        self.driver.close()
        super(LoginSeleniumTest, self).tearDown()
