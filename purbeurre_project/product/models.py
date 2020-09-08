from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.TextField(null=False, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
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

    def substitutes(self):
        return (
            Product.objects.filter(categories__name=self.categories.first())
            .filter(nutrition_grade__lte=self.nutrition_grade)
            .exclude(id=self.id)
            .order_by("nutrition_grade", "energy_100g")
            .distinct("nutrition_grade", "energy_100g")
        )


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
