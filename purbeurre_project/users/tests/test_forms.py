"""Users App forms tests
"""
from django.contrib.auth.models import User
from django.test import TestCase

from users.forms import (AuthenticationFormWithInactiveUsersOkay,
                         UserRegisterForm)


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

    def test_valid_userregisterform(self):
        """Valid if user can use the register form"""
        form = UserRegisterForm(
            data={
                "username": "BobRobert",
                "first_name": "Bob",
                "last_name": "Robert",
                "email": "test_bob@test.com",
                "password1": "fglZfYmr%?,",
                "password2": "fglZfYmr%?,",
                "robot": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_not_match_password_userregisterform(self):
        """Invalid when a password is not match on register form"""
        form = UserRegisterForm(
            data={
                "username": "BobRobert",
                "first_name": "Bob",
                "last_name": "Robert",
                "email": "test_bob@test.com",
                "password1": "fglZfYmr%?,",
                "password2": "ko_fglZfYmr%?,",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_password_userregisterform(self):
        """Invalid register form when password is too short"""
        form = UserRegisterForm(
            data={
                "username": "BobRobert",
                "first_name": "Bob",
                "last_name": "Robert",
                "email": "test_bob@test.com",
                "password1": "ko",
                "password2": "ko",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_user_already_exists_userregisterform(self):
        """Invalid register form when user is already exists"""
        User.objects.create_user(**self.credentials)
        form = UserRegisterForm(
            data={
                "username": "BobRobert",
                "email": "test_bob@test.f",
                "password1": "fglZ9fYmr%?,",
                "password2": "fglZ9fYmr%?,",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())


class LoginTests(TestCase):
    """Login Unit Test"""

    def setUp(self):
        """Login test set up"""
        self.credentials = {"username": "BobRobert", "password": "fglZfYmr%?,"}
        User.objects.create_user(**self.credentials)

    def test_valid_authenticationform(self):
        """Valid authentication form when user exists in db"""
        form = AuthenticationFormWithInactiveUsersOkay(
            data={"username": "BobRobert", "password": "fglZfYmr%?,"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_authenticationform(self):
        """Invalid authentication form when only username is used to login"""
        form = AuthenticationFormWithInactiveUsersOkay(data={"username": "BobRobert"})
        self.assertFalse(form.is_valid())
