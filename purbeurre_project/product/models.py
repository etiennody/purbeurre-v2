from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()
    nutrition_grade = models.CharField(max_length=1)
    quantity = models.TextField()
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
    image_url = models.URLField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class CustomerProduct(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="wanted", on_delete=models.CASCADE
    )
    substitute = models.ForeignKey(
        Product, related_name="healthy", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["customer", "product", "substitute"]]
