"""Unit tests for pages app views
"""
from django.test import TestCase
from django.urls import reverse


class PurbeurrePagesTests(TestCase):
    """Pages tests app

    Args:
        TestCase (class): wraps the tests in two nested atomic() blocks:
        one for the whole class and one for each test.
        Checks the deferred database constraints at the end of each test.
    """
    def test_valid_homepage(self):
        """Test to make sure that our homepage returns an HTTP 200 status code
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_valid_homepage_view(self):
        """Test to make sure that our homepage returns home URL
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_valid_tos_view(self):
        """Test to make sure that our terms of service returns home URL
        """
        response = self.client.get(reverse("tos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/tos.html")

