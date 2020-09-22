from django.test import TestCase
from django.urls import reverse


class PurbeurrePagesTests(TestCase):
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
