"""Mocking tests to processing import data from Open Food Facts Api

Raises:
    Exception: categories from Open Food Facts endpoints is down
    Exception: products from Open Food Facts endpoints is down
"""
# pylint: disable=redefined-outer-name
import pytest
import requests
import responses

from product.management.commands.import_off import Command
from product.models import Category, Product


@pytest.fixture
def mocked_responses():
    """Responses as a pytest fixture

    Yields:
        generator: code block after the yield statement is executed as teardown code
    """
    with responses.RequestsMock() as rsps:
        yield rsps


def test_valid_status_code_api_off_for_categories_is_success(mocked_responses):
    """Valid if status code for categories endpoint import is success

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        body="{}",
        status=200,
        content_type="application/json",
    )
    resp = requests.get("https://fr.openfoodfacts.org/categories.json")
    assert resp.status_code == 200


def test_valid_status_code_api_off_for_products_is_success(mocked_responses):
    """Valid if status code for products endpoint import is success

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        body="{}",
        status=200,
        content_type="application/json",
    )
    resp = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_valid_one_category_populated(mocked_responses):
    """Valid if one category can be populated in database

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={
            "tags": [
                {"name": "pate-a-tartiner", "products": 5002},
                {"name": "Fruits", "products": 5001},
            ]
        },
        status=200,
        content_type="application/json",
    )
    resp = requests.get("https://fr.openfoodfacts.org/categories.json")
    command = Command()
    selected = command.get_populate_categories()
    assert resp.status_code == 200
    assert len(selected) == 2
    assert selected[0]["name"] == "pate-a-tartiner"
    assert selected[0]["products"] == 5002
    assert selected[1]["name"] == "Fruits"
    assert selected[1]["products"] == 5001
    assert Category.objects.filter(name="pate-a-tartiner").exists()


def test_import_categories_max_products(mocked_responses):
    """
    Valid if categories can be import with
    equal or greater than 5000 products

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        status=200,
        json={
            "tags": [
                {"name": "pate-a-tartiner", "products": 2000},
                {"name": "Fruits", "products": 40000},
            ]
        },
    )
    command = Command()
    selected = command.get_populate_categories()
    assert len(selected) == 1
    assert selected[0]["name"] == "Fruits"
    assert selected[0]["products"] == 40000


@pytest.mark.django_db
def test_valid_one_product_populated(mocked_responses):
    """Valid if one product can be populated in database

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={"tags": [{"name": "category_test", "products": 5002}]},
    )
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        json={
            "products": [
                {
                    "product_name": "test",
                    "nutrition_grade_fr": "a",
                    "url": "http://test.fr",
                    "image_front_url": "http://test.fr/test.jpg",
                    "categories": "foo,bar",
                    "nutriments": {
                        "energy_value": "1",
                        "energy_unit": "gr",
                        "carbohydrates_100g": "2",
                        "sugars_100g": "2",
                        "fat_100g": "2",
                        "saturated-fat_100g": "2",
                        "salt_100g": "2",
                        "sodium_100g": "2",
                        "fiber_100g": "2",
                        "proteins_100g": "2",
                    },
                }
            ]
        },
        status=200,
    )
    payload = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": "category_test",
        "sort_by": "unique_scans_n",
        "page_size": 500,
        "json": 1,
    }
    resp_categories = requests.get("https://fr.openfoodfacts.org/categories.json")
    resp_product = requests.get(
        "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
    )
    command = Command()
    command.handle()
    assert resp_categories.status_code == 200
    assert resp_product.status_code == 200
    assert Product.objects.filter(name="test").exists()
    product = Product.objects.get(name="test")
    categ1 = Category.objects.get(name="foo")
    categ2 = Category.objects.get(name="bar")
    assert categ1 in product.categories.all()
    assert categ2 in product.categories.all()


@pytest.mark.django_db
def test_valid_create_products():
    """Valid create_products method with two categories for a product
    """
    command = Command()
    command.create_products(
        [
            {
                "product_name": "test",
                "nutrition_grade_fr": "a",
                "url": "http://test.fr",
                "image_front_url": "http://test.fr/test.jpg",
                "categories": "foo,bar",
                "nutriments": {
                    "energy_value": "1",
                    "energy_unit": "gr",
                    "carbohydrates_100g": "2",
                    "sugars_100g": "2",
                    "fat_100g": "2",
                    "saturated-fat_100g": "2",
                    "salt_100g": "2",
                    "sodium_100g": "2",
                    "fiber_100g": "2",
                    "proteins_100g": "2",
                },
            }
        ]
    )
    product = Product.objects.get(name="test")
    categ1 = Category.objects.get(name="foo")
    categ2 = Category.objects.get(name="bar")
    assert categ1 in product.categories.all()
    assert categ2 in product.categories.all()


@pytest.mark.django_db
def test_valid_existing_category():
    """Valid create_products method if categories exist
    """
    command = Command()
    command.create_products(
        [
            {
                "product_name": "test",
                "nutrition_grade_fr": "a",
                "url": "http://test.fr",
                "image_front_url": "http://test.fr/test.jpg",
                "categories": "foo,bar",
                "nutriments": {
                    "energy_value": "1",
                    "energy_unit": "gr",
                    "carbohydrates_100g": "2",
                    "sugars_100g": "2",
                    "fat_100g": "2",
                    "saturated-fat_100g": "2",
                    "salt_100g": "2",
                    "sodium_100g": "2",
                    "fiber_100g": "2",
                    "proteins_100g": "2",
                },
            }
        ]
    )
    Product.objects.get(name="test")
    Category.objects.get(name="foo")
    Category.objects.get(name="bar")
    assert Category.objects.filter(name="foo").exists()
    assert Category.objects.filter(name="bar").exists()


@responses.activate
def test_import_raises_categories():
    """
    Invalid import data from categories Open Food Fats Api endpoint
    and raise an exception with a message

    Raises:
        Exception: categories from Open Food Facts endpoints is down
    """
    responses.add(
        responses.GET, "https://fr.openfoodfacts.org/categories.json", status=404
    )
    with pytest.raises(Exception):
        command = Command()
        command.get_populate_categories()
        raise Exception("Cannot import categories from Open Food Facts endpoints")


@responses.activate
def test_import_raises_products():
    """
    Invalid import data from products Open Food Fats Api endpoint
    and raise an exception with a message

    Raises:
        Exception: products from Open Food Facts endpoints is down
    """
    responses.add(
        responses.GET, "https://fr.openfoodfacts.org/cgi/search.pl?", status=404
    )
    with pytest.raises(Exception):
        command = Command()
        command.get_populate_categories()
        raise Exception("Cannot import products from Open Food Facts endpoints")
