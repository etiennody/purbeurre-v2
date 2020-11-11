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
        password1.send_keys("fglZfYmr%?,9")
        password2.send_keys("fglZfYmr%?,9")
        submit.click()

        time.sleep(5)
        self.driver.implicitly_wait(5)

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
        user.set_password("fglZfYmr%?,9")
        user.save()
        super(LoginSeleniumTest, self).setUp()

    def test_valid_live_login_page(self):
        """Validate data entries on the login page"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s" % (self.live_server_url))
        self.assertIn("Accueil :: Purbeurre", self.driver.title)

    def tearDown(self):
        self.driver.close()
        super(LoginSeleniumTest, self).tearDown()


class ChangePasswordSeleniumTest(LiveServerTestCase):
    """Change password in functional tests with selenium

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
        user.set_password("fglZfYmr%?,9")
        user.save()
        super(ChangePasswordSeleniumTest, self).setUp()

    def test_valid_live_change_password_page(self):
        """Validate data entries on the change password page"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,9")
        new_password1.send_keys("%h2KtHFJ_%JY")
        new_password2.send_keys("%h2KtHFJ_%JY")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(
            current_url, "%s%s" % (self.live_server_url, "/password_success")
        )
        self.assertIn("Mot de passe modifié :: Purbeurre", self.driver.title)
        self.assertIn(
            "Votre mot de passe a bien été modifié avec succès !",
            self.driver.page_source,
        )

    def test_invalid_live_change_password_with_personal_information(self):
        """Unvalidate data entries on the change password page with personal information"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,9")
        new_password1.send_keys("BobRobert")
        new_password2.send_keys("BobRobert")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/password"))
        self.assertIn(
            "Le mot de passe est trop semblable au champ «&nbsp;nom d’utilisateur&nbsp;».",
            self.driver.page_source,
        )

    def test_invalid_live_change_password_with_only_number(self):
        """Unvalidate data entries on the change password page with only number"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,9")
        new_password1.send_keys("12345678")
        new_password2.send_keys("12345678")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/password"))
        self.assertIn(
            "Ce mot de passe est entièrement numérique.", self.driver.page_source
        )

    def test_invalid_live_change_password_with_short_entries(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,9")
        new_password1.send_keys("Q=3")
        new_password2.send_keys("Q=3")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/password"))
        self.assertIn(
            "Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.",
            self.driver.page_source,
        )

    def test_invalid_live_change_password_with_differents_new_passwords(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,9")
        new_password1.send_keys("tbf:[D=5")
        new_password2.send_keys("kOx`Y{nM")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/password"))
        self.assertIn(
            "Les deux mots de passe ne correspondent pas.",
            self.driver.page_source,
        )

    def test_invalid_live_change_password_with_wrong_old_password(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,9")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("fglZfYmr%?,")
        new_password1.send_keys("kOx`Y{nM")
        new_password2.send_keys("kOx`Y{nM")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/password"))
        self.assertIn(
            "Votre ancien mot de passe est incorrect. Veuillez le rectifier.",
            self.driver.page_source,
        )

    def tearDown(self):
        self.driver.close()
        super(ChangePasswordSeleniumTest, self).tearDown()
