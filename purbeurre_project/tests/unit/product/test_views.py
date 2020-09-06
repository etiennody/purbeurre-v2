from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, SimpleTestCase, TestCase, TransactionTestCase
from django.urls import reverse

from product.models import Category, CustomerProduct, Product


class ProductTest(TestCase):
    """Product tests app

    Args:
        TestCase (class): wraps the tests in two nested atomic() blocks:
        one for the whole class and one for each test.
        Checks the deferred database constraints at the end of each test.
    """

    def setUp(self):
        """Initialyze the set up tests"""
        user = User.objects.create(
            username="BobRobert",
            first_name="Bob",
            last_name="Robert",
            email="test_bob@test.com",
        )
        user.set_password("fglZfYmr%?,")
        user.save()

        category = Category.objects.create(name="Categorie test")

        number_of_products = 13
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

    # product views
    def test_valid_search_results_url_and_template(self):
        response = self.client.get(reverse("search"), {"q": "Product 1"})
        self.assertTemplateUsed(response, "product/search_results.html")
        self.assertEqual(response.status_code, 200)

    def test_valid_search_results_url_404(self):
        response = self.client.get(reverse("search"), {"q": "Product 1", "page": "@"})
        self.assertEqual(response.status_code, 404)

    def test_valid_search_results_contains_good_query(self):
        response = self.client.get(reverse("search"), {"q": "Product 1"})
        self.assertContains(response, "Product 1")

    def test_valid_search_results_product_found(self):
        response = self.client.get(reverse("search"), {"q": "Product 2"})
        self.assertEqual(response.context_data["object_list"].count(), 1)

    def test_invalid_search_results_product_ko(self):
        response = self.client.get(reverse("search"), {"q": "Moutarde"})
        self.assertEqual(response.context_data["object_list"].count(), 0)

    def test_valid_search_pagination_is_six(self):
        response = self.client.get(reverse("search"), {"q": "Product"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context_data["object_list"]), 6)

    # substitute views
    def test_valid_substitute_results_url_and_template(self):
        response = self.client.get(reverse("substitute", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/substitute_results.html")

    def test_valid_substitute_better_nutriscore_or_equivalent_and_exclude_id(self):
        response = self.client.get(reverse("substitute", args=["3"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object_list"].count(), 1)
        if not Product.objects.get(id=3) in response.context_data["object_list"]:
            exclude_id = True
        self.assertTrue(exclude_id)

    def test_valid_substitute_without_products(self):
        junk_product = Product.objects.create(
            id=14,
            name="Product 14",
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
            image_url=f"http://www.test-product14.fr/product.jpg",
            url=f"http://www.test-product14.fr",
        )
        response = self.client.get(reverse("substitute", args=["14"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object_list"].count(), 0)

    # details views
    def test_valid_product_detail_view(self):
        product = Product.objects.get(name="Product 1")
        response = self.client.get(reverse("details", args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/product_details.html")

    def test_invalid_product_details_results(self):
        response = self.client.get(reverse("details", args=["666"]))
        self.assertTrue(response.status_code, 404)

    # save views
    def test_valid_save_page_if_not_logged(self):
        product = Product.objects.get(name="Product 1")
        substitute = Product.objects.get(name="Product 2")
        response = self.client.get(reverse("save"), args=(product.id, substitute.id))
        self.assertRedirects(
            response,
            "/login/?next=/save/",
            status_code=302,
            target_status_code=200,
        )

    def test_valid_save_view_if_logged(self):
        self.assertTrue(self.client.login(username="BobRobert", password="fglZfYmr%?,"))
        customer = User.objects.get(username="BobRobert").id
        product_id = Product.objects.get(name="Product 1").id
        substitute_id = Product.objects.get(name="Product 2").id
        response = self.client.get(
            reverse("save"), args=(customer, product_id, substitute_id)
        )
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, "/favorites/", status_code=302, target_status_code=200
        )

    # favorites views
    def test_valid_favorites_redirect_template_if_not_logged(self):
        response = self.client.get(reverse("favorites"))
        self.assertTemplateUsed(response, "product/favorites.html")

    def test_valid_favorites_template_if_logged_with_any_product(self):
        self.assertTrue(self.client.login(username="BobRobert", password="fglZfYmr%?,"))
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/favorites.html")
        self.assertEqual(response.context_data["object_list"].count(), 0)

    def test_valid_favorites_if_logged_with_one_product(self):
        self.assertTrue(self.client.login(username="BobRobert", password="fglZfYmr%?,"))
        user_id = User.objects.get(username="BobRobert").id
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.context_data["object_list"].all().count(), 0)
        response = self.client.post(
            reverse("save"),
            {
                "product_id": Product.objects.get(id=1).id,
                "substitute_id": Product.objects.get(id=2).id,
                "customer": user_id,
                "next": "/",
            },
        )
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.context_data["object_list"].all().count(), 1)
        self.assertEqual(response.status_code, 200)

    # delete views
    def test_invalid_delete_if_not_logged(self):
        response = self.client.post("/delete/5")
        self.assertRedirects(
            response,
            "/login/?next=/delete/5",
            status_code=302,
            target_status_code=200,
        )

    def test_invalid_delete_if_logged_and_unknown_substitute_id(self):
        self.assertTrue(self.client.login(username="BobRobert", password="fglZfYmr%?,"))
        response = self.client.post("/delete/1000")
        self.assertEqual(response.status_code, 404)

    def test_valid_delete_if_logged(self):
        self.assertTrue(self.client.login(username="BobRobert", password="fglZfYmr%?,"))
        user_id = User.objects.get(username="BobRobert").id
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.context_data["object_list"].count(), 0)
        response = self.client.post(
            reverse("save"),
            {
                "customer": user_id,
                "product_id": Product.objects.get(id=1).id,
                "substitute_id": Product.objects.get(id=2).id,
                "next": "/",
            },
        )
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.context_data["object_list"].count(), 1)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/delete/1")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.context_data["object_list"].count(), 0)


class Test404(SimpleTestCase):
    """Test the page error 404

    Args:
        SimpleTestCase (class): a subclass of unittest.TestCase that adds more functionality
    """

    def test_valid_error_404_page_view(self):
        response = self.client.get("/url_error")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.templates[0].name, "404.html")
