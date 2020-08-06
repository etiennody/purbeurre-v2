from django.test import TestCase


class PurbeurrePagesTests(TestCase):
    def test_homepage(self):
        """Test to make sure that our homepage returns an HTTP 200 status code
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
