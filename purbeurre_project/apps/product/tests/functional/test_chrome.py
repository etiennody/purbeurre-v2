"""Functional tests for product app
"""
import time
import unittest

from django.test import LiveServerTestCase
from product.models import Category, Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class SearchResultsPageSeleniumTest(LiveServerTestCase):
    """Search results functional test with selenium

    Args:
        LiveServerTestCase (class): Do basically the same as TransactionTestCase but also launch a live HTTP server in a separate thread so that the tests use another testing framework, as Selenium, instead of the built-in dummy client.
    """

    def setUp(self):
        Product.objects.create(
            name="Nutella",
            nutrition_grade="e",
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
            image_url=f"http://www.test-product-nutella.fr/product.jpg",
            url=f"http://www.test-product-nutella.fr",
        )
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def test_valid_live_search_results_page_title__and_product_present(self):
        """Valid if search results title and product searched are present

        Raises:
            Exception: message to inform access is denied on search results page
        """
        self.driver.get("%s%s" % (self.live_server_url, "/search/?q=nutella"))
        if not "Résultats recherche produits :: Purbeurre" in self.driver.title:
            raise Exception("Unable to load purbeurre search results page!")
        self.assertIn("Résultats recherche produits :: Purbeurre", self.driver.title)
        self.assertIn("Nutella", self.driver.page_source)

    def tearDown(self):
        self.driver.close()


class SubstituteResultsPageSeleniumTest(LiveServerTestCase):
    """Substitute result functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        categ1 = Category.objects.create(name="category_a")
        categ2 = Category.objects.create(name="category_b")
        categ3 = Category.objects.create(name="category_c")
        categ4 = Category.objects.create(name="category_d")
        prod1 = Product.objects.create(
            name="Nutella",
            nutrition_grade="d",
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
            image_url="http://www.test-nutella.fr/product.jpg",
            url="http://www.test-nutella.fr",
        )
        categ1.product_set.add(prod1)
        categ2.product_set.add(prod1)
        categ3.product_set.add(prod1)
        categ4.product_set.add(prod1)
        prod2 = Product.objects.create(
            name="Noisetti",
            nutrition_grade="a",
            energy_100g="3",
            energy_unit="gr",
            carbohydrates_100g="2",
            sugars_100g="2",
            fat_100g="2",
            saturated_fat_100g="2",
            salt_100g="0.2",
            sodium_100g="0.2",
            fiber_100g="0.2",
            proteins_100g="0.2",
            image_url="http://www.test-noisetti.fr/product.jpg",
            url="http://www.test-noisetti.fr",
        )
        categ1.product_set.add(prod2)
        categ2.product_set.add(prod2)
        categ3.product_set.add(prod2)
        categ4.product_set.add(prod2)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def test_valid_live_substitute_results_page(self):
        """Valid substitute results page"""
        self.driver.get("%s" % (self.live_server_url))
        text = self.driver.find_element(By.ID, "inputSearchForm")
        submit = self.driver.find_element(By.CLASS_NAME, "btn")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        text.send_keys("product")
        submit.click()
        self.driver.get("%s%s" % (self.live_server_url, "/search/?q=nutella"))
        product = self.driver.find_element(By.CLASS_NAME, "get-more")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        product.click()
        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "%s%s" % (self.live_server_url, "/substitute/5"))
        self.assertIn("Résultats recherche substituts :: Purbeurre", self.driver.title)
        self.assertIn(
            "Vous pouvez remplacer cet aliment par :", self.driver.page_source
        )
        self.assertIn("Noisetti", self.driver.page_source)

    def tearDown(self):
        self.driver.close()
