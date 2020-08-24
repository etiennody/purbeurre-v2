from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from product.models import Category, Product


def db_init():
    """ setUp Test """

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
        image_url="http://www.test-jus.fr",
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
        image_url="http://www.test-rooibos.fr",
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
        image_url="http://www.test-limonade.fr",
    )


class ProductTest(TestCase):
    """ Test Product App """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.search_url = reverse("search")
        db_init()

    # product views
    def test_valid_search_results_url_and_template(self):
        response = self.client.get(self.search_url + "?q=Jus")
        self.assertTemplateUsed(response, "product/search_results.html")
        self.assertEqual(response.status_code, 200)

    def test_valid_search_results_url_404(self):
        response = self.client.get(self.search_url + "?q=Jus&page=@")
        self.assertEqual(response.status_code, 404)

    def test_valid_search_results_contains_good_query(self):
        response = self.client.get(self.search_url + "?q=Limonade")
        self.assertContains(response, "Limonade")

    def test_valid_search_results_product_found(self):
        response = self.client.get(self.search_url + "?q=Rooibos")
        self.assertEqual(response.context_data["object_list"].count(), 1)

    def test_invalid_search_results_product_ko(self):
        response = self.client.get(self.search_url + "?q=moutarde")
        self.assertEqual(response.context_data["object_list"].count(), 0)

    # substitute views
    def test_valid_substitute_results_url_and_template(self):
        response = self.client.get("/substitute/1")
        self.assertTemplateUsed(response, "product/substitute_results.html")
        self.assertEqual(response.status_code, 200)

    def test_substitute_better_nutriscore_or_equivalent_and_exclude_id(self):
        response = self.client.get("/substitute/3")
        self.assertEqual(response.status_code, 200)
        if Product.objects.get(id=2) in response.context_data["object_list"]:
            exclude_id = True
        self.assertTrue(exclude_id)


class ImportOffTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command("import_off", stdout=out)
        self.assertIn("Data successfully downloaded !", out.getvalue())


class CommandTest(TransactionTestCase):
    """ Test BaseCommand with mock and patch"""

    @patch("product.management.commands.import_off", new_callable=bool)
    def test_import_off_errors(self, mock):
        mock = False

        with self.assertRaises(TypeError):
            call_command("import_off", nutriscore="o")

        with self.assertRaises(TypeError):
            call_command("import_off", category=12)
