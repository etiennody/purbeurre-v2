"""Product app models
"""
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Category model maps to a category database table

    Args:
        models (subclass): a python class that subclasses django.db.models.Model
    """

    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model maps to a product database table

    Args:
        models (subclass): a python class that subclasses django.db.models.Model
    """

    name = models.TextField(null=False, unique=True)
    nutrition_grade = models.CharField(max_length=1)
    energy_100g = models.IntegerField()
    energy_unit = models.TextField()
    carbohydrates_100g = models.FloatField()
    sugars_100g = models.FloatField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    sodium_100g = models.FloatField()
    fiber_100g = models.FloatField()
    proteins_100g = models.FloatField()
    url = models.URLField(unique=True, null=True)
    image_url = models.URLField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def substitutes(self, nb_common_categories=4):
        """Substitute method to find healthy product matching with categories

        Args:
            nb_common_categories (int, optional): number of categories
            which are match with categories product searched.
            Defaults to 4.

        Returns:
            list: collection of substitute product objects from database
        """
        related_products = (
            self.categories.through.objects.all()
            .filter(
                product__nutrition_grade__lte=self.nutrition_grade,
                category__in=self.categories.all(),
            )
            .values("product_id")
            .annotate(matches=models.Count("category_id"))
            .filter(matches__gte=nb_common_categories)
            .order_by("-matches")
            .values_list("product_id")
        )

        return (
            Product.objects.filter(pk__in=related_products)
            .exclude(id=self.id)
            .order_by("nutrition_grade", "energy_100g")
            .distinct("nutrition_grade", "energy_100g")
        )


class CustomerProduct(models.Model):
    """Customer Product model maps to favorites database table

    Args:
        models (subclass): a python class that subclasses django.db.models.Model
    """

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="wanted", on_delete=models.CASCADE
    )
    substitute = models.ForeignKey(
        Product, related_name="healthy", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["customer", "product", "substitute"]]
