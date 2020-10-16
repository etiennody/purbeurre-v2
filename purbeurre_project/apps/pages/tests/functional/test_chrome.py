"""Functional test for pages app
"""
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from product.models import Category, Product


@unittest.skip("homepage class skipping")
class HomepageSeleniumTest(unittest.TestCase):
    """Homepage functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--window-size=1920x1080')
        self.driver = webdriver.Chrome(chrome_options=chrome_options
        )
        Category.objects.create(name="test")
        number_of_products = 12
        for product in range(number_of_products):
            Product.objects.create(
                id=f"{product}",
                name=f"Product {product}",
                nutrition_grade="b",
                energy_100g="2",
                energy_unit="gr",
                carbohydrates_100g="2",
                sugars_100g="2",
                fat_100g="2",
                saturated_fat_100g="2",
                salt_100g="0.2",
                sodium_100g="0.2",
                fiber_100g="0.2",
                proteins_100g="0.2",
                image_url=f"http://www.test-product{product}.fr/product.jpg",
                url=f"http://www.test-product{product}.fr",
            )

    def test_valid_live_home_page_title_is_present(self):
        """Valid if homepage title exists

        Raises:
            Exception: message to inform access is denied on homepage
        """
        self.driver.get("https://purbeurre.etiennody.fr/")
        if not "Accueil :: Purbeurre" in self.driver.title:
            raise Exception("Unable to load purbeurre homepage!")
        self.assertIn("Accueil :: Purbeurre", self.driver.title)

    def tearDown(self):
        self.driver.close()
