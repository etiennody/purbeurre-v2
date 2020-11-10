"""
The custom management command import_off is used to run a stand-alone script
to import data from Open Food Facts.
"""
import json

import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from product.models import Category, Product


class Command(BaseCommand):
    """
    Command class is used to import categories and products
    from Open Food Facts Api

    Args:
        BaseCommand (class): analyze the command line parameters,
        which are used to determine the code to be called consequently
    """

    help = "Import data from Open Food Facts API"

    def get_populate_categories(self):
        """
        Method to populate all categories containing
        greater than or equal to 5000 products

        Args:
            url_categories (string): endpoint Open Food Facts Api for categories

        Returns:
            list: all categories selected
        """
        url_categories = "https://fr.openfoodfacts.org/categories.json"
        print("Requesting categories")
        category_response = requests.get(url=url_categories)
        if category_response.status_code != 200:
            self.stdout.write(
                self.style.ERROR(
                    "Searching for category with the Open Food Facts API is not available."
                )
            )
        categories = json.loads(category_response.content)["tags"]
        categories_selected = [
            categ for categ in categories if categ["products"] >= 3000
        ]
        for category in categories_selected:
            try:
                with transaction.atomic():
                    categ = Category(name=category["name"])
                    categ.save()
            except Exception as exx:
                print("Une des catégories n'a pu être importée, voici l'erreur:", exx)
        return categories_selected

    def get_products_for_category(self, category_name):
        """Import products for each category selected

        Args:
            category_name (string): a name of category

        Returns:
            list: list of product dictionnary
        """
        url_products = "https://fr.openfoodfacts.org/cgi/search.pl?"
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category_name,
            "sort_by": "unique_scans_n",
            "page_size": 500,
            "json": 1,
        }
        print(f"Requesting products for category of {category_name}")
        product_response = requests.get(url=url_products, params=payload)
        if product_response.status_code != 200:
            self.stdout.write(
                self.style.ERROR(
                    "Searching for products with the Open Food Facts API is not available."
                )
            )
        return json.loads(product_response.content)["products"]

    def validate_product_dict(self, product_dict):
        """Help validate import product when it calls on nutriments

        Args:
            product_dict (dictionnary): a dictionnary of product selected

        Returns:
            boolean: true when elements are required
        """
        for required in ["nutrition_grade_fr"]:
            if not product_dict.get(required, "").strip():
                return False
        if not product_dict["nutriments"].get("fiber_100g", 0):
            return False
        return True

    def update_product(self, product, data):
        """Method to update database with existing products

        Args:
            product (object): from Product model
            data (dictionnary): elements making up a product
        """
        try:
            with transaction.atomic():
                product.name = data.get("product_name")
                product.nutrition_grade = data.get("nutrition_grade_fr")
                product.energy_100g = data["nutriments"].get("energy_value")
                product.energy_unit = data["nutriments"].get("energy_unit")
                product.carbohydrates_100g = data["nutriments"].get(
                    "carbohydrates_100g"
                )
                product.sugars_100g = data["nutriments"].get("sugars_100g")
                product.fat_100g = data["nutriments"].get("fat_100g")
                product.saturated_fat_100g = data["nutriments"].get(
                    "saturated-fat_100g"
                )
                product.salt_100g = data["nutriments"].get("salt_100g")
                product.sodium_100g = data["nutriments"].get("sodium_100g")
                product.fiber_100g = data["nutriments"].get("fiber_100g")
                product.proteins_100g = data["nutriments"].get("proteins_100g")
                product.url = data.get("url")
                product.image_url = data.get("image_front_url")
                product.save()
        except IntegrityError:
            product.delete()

    def create_product(self, data):
        """Method to create products and add categories with the related product

        Args:
            data (dictionnary): elements making up a product
        """
        product = Product.objects.create(
            name=data.get("product_name"),
            nutrition_grade=data.get("nutrition_grade_fr"),
            energy_100g=data["nutriments"].get("energy_value"),
            energy_unit=data["nutriments"].get("energy_unit"),
            carbohydrates_100g=data["nutriments"].get("carbohydrates_100g"),
            sugars_100g=data["nutriments"].get("sugars_100g"),
            fat_100g=data["nutriments"].get("fat_100g"),
            saturated_fat_100g=data["nutriments"].get("saturated-fat_100g"),
            salt_100g=data["nutriments"].get("salt_100g"),
            sodium_100g=data["nutriments"].get("sodium_100g"),
            fiber_100g=data["nutriments"].get("fiber_100g"),
            proteins_100g=data["nutriments"].get("proteins_100g"),
            url=data.get("url"),
            image_url=data.get("image_front_url"),
        )
        print(".", end="")
        category_list = data.get("categories")
        for category_product in category_list.split(","):
            catego, _ = Category.objects.get_or_create(name=category_product)
            product.categories.add(catego)

    def populate_products(self, products_list):
        """Method to populate database with products

        Args:
            products_list (list): a list of products that can be used to create new ones
        """

        for product_dict in products_list:
            if not self.validate_product_dict(product_dict):
                print("S", end="")
                continue
            # if product exists on DB
            if Product.objects.filter(name=product_dict.get("product_name")).exists():
                # update product
                self.update_product(
                    product=Product.objects.get(name=product_dict.get("product_name")),
                    data=product_dict,
                )
            else:
                try:
                    # create product
                    self.create_product(product_dict)
                except Exception as exx:
                    print("Un des produits n'a pu être importé, voici l'erreur :", exx)

    def handle(self, *args, **options):
        """Main method to download data from Open Food Facts API"""
        self.stdout.write("Product downloads in progress...")
        # Process for products
        for category in self.get_populate_categories():
            products = self.get_products_for_category(category["name"])
            self.populate_products(products)
        self.stdout.write(self.style.SUCCESS("Data successfully downloaded !"))
