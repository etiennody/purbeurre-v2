from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from product.models import Category, CustomerProduct, Product


class ProductTest(TestCase):
    """ Test Product App """

    def setUp(self):
        """Initialyze the set up tests"""
        user = User.objects.create(
            username="BobRobert",
            first_name="Bob",
            last_name="Robert",
            email="test_bob@test.com",
            password="fglZfYmr%?,",
        )

        category = Category.objects.create(name="Boissons")

        jus = Product.objects.create(
            id="1",
            name="Jus",
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
            image_url="http://www.test-jus.fr/jus.jpg",
            url="http://www.test-jus.fr",
        )
        rooibos = Product.objects.create(
            id="2",
            name="Rooibos",
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
            image_url="http://www.test-rooibos.fr/rooibos.jpg",
            url="http://www.test-rooibos.fr",
        )
        limonade = Product.objects.create(
            id="3",
            name="Limonade",
            nutrition_grade="c",
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
            image_url="http://www.test-limonade.fr/limonade.jpg",
            url="http://www.test-limonade.fr",
        )

    # product views
    def test_valid_search_results_url_and_template(self):
        response = self.client.get(reverse("search"), {"q": "Jus"})
        self.assertTemplateUsed(response, "product/search_results.html")
        self.assertEqual(response.status_code, 200)

    def test_valid_search_results_url_404(self):
        response = self.client.get(reverse("search"), {"q": "Jus", "page": "@"})
        self.assertEqual(response.status_code, 404)

    def test_valid_search_results_contains_good_query(self):
        response = self.client.get(reverse("search"), {"q": "Limonade"})
        self.assertContains(response, "Limonade")

    def test_valid_search_results_product_found(self):
        response = self.client.get(reverse("search"), {"q": "Rooibos"})
        self.assertEqual(response.context_data["object_list"].count(), 1)

    def test_invalid_search_results_product_ko(self):
        response = self.client.get(reverse("search"), {"q": "Moutarde"})
        self.assertEqual(response.context_data["object_list"].count(), 0)

    # substitute views
    def test_valid_substitute_results_url_and_template(self):
        response = self.client.get(reverse("substitute", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/substitute_results.html")

    def test_substitute_better_nutriscore_or_equivalent_and_exclude_id(self):
        response = self.client.get(reverse("substitute", args=["3"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object_list"].count(), 2)
        if Product.objects.get(id=1) in response.context_data["object_list"]:
            exclude_id = True
        self.assertTrue(exclude_id)

    # details views
    def test_valid_product_detail_view(self):
        product = Product.objects.get(name="Jus")
        response = self.client.get(reverse("details", args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/product_details.html")

    def test_invalid_product_details_results(self):
        response = self.client.get(reverse("details", args=["666"]))
        self.assertTrue(response.status_code, 404)

    # save views
    def test_valid_save_page_if_not_logged(self):
        product = Product.objects.get(name="Jus")
        substitute = Product.objects.get(name="Rooibos")
        response = self.client.get(reverse("save"), args=(product.id, substitute.id))
        self.assertRedirects(
            response, "/login/?next=/save/", status_code=302, target_status_code=200,
        )

    def test_valid_save_view_if_logged(self):
        self.client.login(username="BobRobert", password="fglZfYmr%?,")
        customer = User.objects.get(username="BobRobert").id
        product = Product.objects.get(name="Jus")
        substitute = Product.objects.get(name="Rooibos")
        response = self.client.post(
            reverse("save"), args=(customer, product.id, substitute.id)
        )
        self.assertTrue(response.status_code, 200)

    # favorites views
    def test_valid_favorites_redirect_template_if_not_logged(self):
        response = self.client.get(reverse("favorites"))
        self.assertTemplateUsed(response, "product/favorites.html")

    def test_favorites_if_logged_and_zero_product(self):
        self.client.login(username="BobRobert", password="fglZfYmr%?,")
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/favorites.html")
        self.assertEqual(response.context_data["object_list"].count(), 0)

    # test views
    def test_delete_if_not_logged(self):
        response = self.client.post("/delete/1000")
        self.assertRedirects(
            response,
            "/login/?next=/delete/1000",
            status_code=302,
            target_status_code=200,
        )
