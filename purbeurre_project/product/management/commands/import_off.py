import json

import requests
from django.core.management.base import BaseCommand

from product.models import Category, Product


class Command(BaseCommand):
    help = "Import data from Open Food Facts API"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Cleaning Product and Category tables successfully!")
        )

        self.stdout.write("Product downloads in progress...")

        # Process for categories
        url = "https://fr.openfoodfacts.org/categories.json"

        category_response = requests.get(url=url)
        if category_response.status_code != 200:
            self.stdout.write(
                self.style.ERROR(
                    "Searching for category with the Open Food Facts API is not available."
                )
            )
        categories = json.loads(category_response.content)["tags"]
        categories_selected = [
            categ for categ in categories if categ["products"] >= 5000
        ]

        for category in categories_selected:
            try:
                categ = Category(name=category["name"])
                categ.save()
            except:
                pass

            # Process for products
            url = "https://fr.openfoodfacts.org/cgi/search.pl?"
            payload = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": category["name"],
                "sort_by": "unique_scans_n",
                "page_size": 500,
                "json": 1,
            }
            product_response = requests.get(url=url, params=payload)
            if product_response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(
                        "Searching for products with the Open Food Facts API is not available."
                    )
                )
            products = json.loads(product_response.content)["products"]
            for product in products:
                try:
                    new_product = categ.product_set.create(
                        name=product.get("product_name"),
                        nutrition_grade=product.get("nutrition_grade_fr"),
                        energy_100g=product["nutriments"].get("energy_value"),
                        energy_unit=product["nutriments"].get("energy_unit"),
                        carbohydrates_100g=product["nutriments"].get(
                            "carbohydrates_100g"
                        ),
                        sugars_100g=product["nutriments"].get("sugars_100g"),
                        fat_100g=product["nutriments"].get("fat_100g"),
                        saturated_fat_100g=product["nutriments"].get(
                            "saturated-fat_100g"
                        ),
                        salt_100g=product["nutriments"].get("salt_100g"),
                        sodium_100g=product["nutriments"].get("sodium_100g"),
                        fiber_100g=product["nutriments"].get("fiber_100g"),
                        proteins_100g=product["nutriments"].get("proteins_100g"),
                        image_url=product.get("image_front_url"),
                    )
                except Exception as e:
                    pass
        self.stdout.write(self.style.SUCCESS("Data successfully downloaded !"))
