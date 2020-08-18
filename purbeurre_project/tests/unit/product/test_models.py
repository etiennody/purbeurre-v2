import pytest
from django.test import TestCase

from product.models import Category, Product


class ProductModelTest(TestCase):
    """Product Model Tests

    Args:
        TestCase (subclass): confirm test classes as subclasses of django.test.TestCase
    """

    def test_product__str__(self):
        """Test the __str__() on Product model method. 
        """
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
        """Test if a product can have two categories.
        """
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
    """Ctaegory Model Tests

    Args:
        TestCase (subclass): confirm test classes as subclasses of django.test.TestCase
    """

    def test_category__str__(self):
        """Test the __str__() on Category model method. 
        """
        category = Category.objects.create(id="1", name="pate-a-tartiner",)
        self.assertTrue(category.__str__() == "pate-a-tartiner")
        self.assertTrue(str(category) == "pate-a-tartiner")

    def test_categories_have_a_product(self):
        """Test if two categories can have a product.
        """
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
        category1.product_set.add(product)
        category2.product_set.add(product)
        self.assertEqual(product.categories.count(), 2)
