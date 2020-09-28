"""Unit tests for product app models
"""
from django.test import TestCase

from product.models import Category, Product


class ProductModelTest(TestCase):
    """Product Model Tests

    Args:
        TestCase (subclass): confirm test classes as subclasses of django.test.TestCase
    """

    def test_product__str__(self):
        """Test the __str__() on Product model method"""
        product = Product.objects.create(
            id="1",
            name="Nutella",
            nutrition_grade="a",
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
            image_url="http://www.test.fr",
        )
        self.assertTrue(product.__str__() == "Nutella")
        self.assertTrue(str(product) == "Nutella")

    def test_product_has_two_categories(self):
        """Test if a product can have two categories"""
        product = Product.objects.create(
            id="1",
            name="Nutella",
            nutrition_grade="a",
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
            image_url="http://www.test.fr",
        )
        category1 = Category.objects.create(name="Category1")
        category2 = Category.objects.create(name="Category2")
        product.categories.set([category1.pk, category2.pk])
        self.assertEqual(product.categories.count(), 2)


class CategoryModelTest(TestCase):
    """Category Model Tests

    Args:
        TestCase (subclass): confirm test classes as subclasses of django.test.TestCase
    """

    def test_category__str__(self):
        """Test the __str__() on Category model method"""
        category = Category.objects.create(
            id="1",
            name="pate-a-tartiner",
        )
        self.assertTrue(category.__str__() == "pate-a-tartiner")
        self.assertTrue(str(category) == "pate-a-tartiner")

    def test_categories_have_a_product(self):
        """Test if two categories can have a product"""
        product = Product.objects.create(
            id="1",
            name="Product",
            nutrition_grade="a",
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
            image_url="http://www.test-product.fr/product.jpg",
            url="http://www.test-product.fr",
        )
        category1 = Category.objects.create(name="Category1")
        category2 = Category.objects.create(name="Category2")
        category1.product_set.add(product)
        category2.product_set.add(product)
        self.assertEqual(product.categories.count(), 2)


class ProductSubstituteTest(TestCase):
    """Test substitute method in Product Model

    Args:
        TestCase (subclass): confirm test classes as subclasses of django.test.TestCase
    """

    def test_valid_substitutes_query(self):
        """Valid if sustitutes query works with added products categories"""
        categ1 = Category.objects.create(name="category_a")
        categ2 = Category.objects.create(name="category_b")
        prod1 = Product.objects.create(
            name="Product 15",
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
            image_url="http://www.test-product15.fr/product.jpg",
            url="http://www.test-product15.fr",
        )
        categ1.product_set.add(prod1)
        categ2.product_set.add(prod1)
        prod2 = Product.objects.create(
            name="Product 16",
            nutrition_grade="a",
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
            image_url="http://www.test-product16.fr/product.jpg",
            url="http://www.test-product16.fr",
        )
        categ1.product_set.add(prod2)
        categ2.product_set.add(prod2)
        prod3 = Product.objects.create(
            name="Product 17",
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
            image_url="http://www.test-product17.fr/product.jpg",
            url="http://www.test-product17.fr",
        )
        prod3.categories.add(categ1)
        response = prod1.substitutes(nb_common_categories=2)
        print(str(response.query))
        self.assertEqual(response.count(), 1)
        self.assertEqual(list(response), [prod2])

    def test_invalid_substitutes_query(self):
        """Valid if sustitutes query return any product"""
        categ1 = Category.objects.create(name="category_a")
        categ2 = Category.objects.create(name="category_b")
        prod1 = Product.objects.create(
            id="15",
            name="Product 15",
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
            image_url="http://www.test-product15.fr/product.jpg",
            url="http://www.test-product15.fr",
        )
        categ1.product_set.add(prod1)
        categ2.product_set.add(prod1)
        prod2 = Product.objects.create(
            id="16",
            name="Product 16",
            nutrition_grade="a",
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
            image_url="http://www.test-product16.fr/product.jpg",
            url="http://www.test-product16.fr",
        )
        categ1.product_set.add(prod2)
        categ2.product_set.add(prod2)
        prod3 = Product.objects.create(
            id="17",
            name="Product 17",
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
            image_url="http://www.test-product17.fr/product.jpg",
            url="http://www.test-product17.fr",
        )
        categ2.product_set.add(prod3)
        response = prod2.substitutes(nb_common_categories=2)
        print(str(response.query))
        self.assertEqual(response.count(), 0)
        self.assertEqual(list(response), [])
