"""Mocking tests to processing import data from Open Food Facts Api

Raises:
    Exception: categories from Open Food Facts endpoints is down
    Exception: products from Open Food Facts endpoints is down
"""
# pylint: disable=redefined-outer-name
import pytest
import requests
import responses
from product.management.commands.import_off import Command as command_import
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
def test_valid_one_category_populated_in_db(mocked_responses):
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
    command = command_import()
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
    command = command_import()
    selected = command.get_populate_categories()
    assert len(selected) == 1
    assert selected[0]["name"] == "Fruits"
    assert selected[0]["products"] == 40000


@pytest.mark.django_db
def test_valid_one_product_was_populated_in_db(mocked_responses):
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
    command = command_import()
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
def test_valid_populated_products():
    """Valid create_products method with two categories for a product"""
    command = command_import()
    command.populate_products(
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
    """Valid create_products method if categories exist"""
    command = command_import()
    command.populate_products(
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
        command = command_import()
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
        command = command_import()
        command.get_populate_categories()
        raise Exception("Cannot import products from Open Food Facts endpoints")


@pytest.mark.django_db
def test_valid_update_one_product_nutriscore_a_to_b_populated(mocked_responses):
    """Valid if a product can be updated with nutriscore a to b in database

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    product = Product.objects.create(
        name="ProductA",
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
        image_url="http://www.test-product.fr/product.jpg",
        url="http://www.test-product.fr",
    )
    category = Category.objects.create(name="bar")
    category.product_set.add(product)
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={"tags": [{"name": "foo", "products": 5002}]},
    )
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        json={
            "products": [
                {
                    "product_name": "ProductA",
                    "nutrition_grade_fr": "b",
                    "url": "http://www.test-product.fr",
                    "image_front_url": "http://www.test-product.fr/product.jpg",
                    "categories": "foo",
                    "nutriments": {
                        "energy_value": "1",
                        "energy_unit": "gr",
                        "carbohydrates_100g": "2",
                        "sugars_100g": "2",
                        "fat_100g": "2",
                        "saturated-fat_100g": "2",
                        "salt_100g": "0.2",
                        "sodium_100g": "0.2",
                        "fiber_100g": "0.2",
                        "proteins_100g": "0.2",
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
        "tag_0": "foo",
        "sort_by": "unique_scans_n",
        "page_size": 500,
        "json": 1,
    }
    resp_categories = requests.get("https://fr.openfoodfacts.org/categories.json")
    resp_product = requests.get(
        "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
    )
    command = command_import()
    command.handle()
    assert resp_categories.status_code == 200
    assert resp_product.status_code == 200
    assert Product.objects.filter(name="ProductA").exists()
    assert Product.objects.filter(nutrition_grade="b").exists()
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_valid_noupdate_for_one_product(mocked_responses):
    """Valid if a product can be updated without changes in database

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    product = Product.objects.create(
        name="ProductA",
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
        image_url="http://www.test-product.fr/product.jpg",
        url="http://www.test-product.fr",
    )
    category = Category.objects.create(name="bar")
    category.product_set.add(product)
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={"tags": [{"name": "bar", "products": 5002}]},
    )
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        json={
            "products": [
                {
                    "product_name": "ProductA",
                    "nutrition_grade_fr": "a",
                    "url": "http://www.test-product.fr",
                    "image_front_url": "http://www.test-product.fr/product.jpg",
                    "categories": "bar",
                    "nutriments": {
                        "energy_value": "2",
                        "energy_unit": "gr",
                        "carbohydrates_100g": "2",
                        "sugars_100g": "2",
                        "fat_100g": "2",
                        "saturated-fat_100g": "2",
                        "salt_100g": "0.2",
                        "sodium_100g": "0.2",
                        "fiber_100g": "0.2",
                        "proteins_100g": "0.2",
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
        "tag_0": "bar",
        "sort_by": "unique_scans_n",
        "page_size": 500,
        "json": 1,
    }
    resp_categories = requests.get("https://fr.openfoodfacts.org/categories.json")
    resp_product = requests.get(
        "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
    )
    command = command_import()
    command.handle()
    assert resp_categories.status_code == 200
    assert resp_product.status_code == 200
    assert Product.objects.filter(name="ProductA").exists()
    assert Product.objects.filter(nutrition_grade="a").exists()
    categ_bar = Category.objects.get(name="bar")
    assert categ_bar in product.categories.all()
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_valid_updating_and_new_product_in_same_category(mocked_responses):
    """Valid if a product a can be updated with another product b to be added

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    product_a = Product.objects.create(
        name="ProductA",
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
        image_url="http://www.test-product-a.fr/product-a.jpg",
        url="http://www.test-product-a.fr",
    )
    category = Category.objects.create(name="foo")
    category.product_set.add(product_a)
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={
            "tags": [
                {"name": "foo", "products": 5002},
            ]
        },
    )
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        json={
            "products": [
                {
                    "product_name": "ProductA",
                    "nutrition_grade_fr": "a",
                    "url": "http://www.test-product-a.fr",
                    "image_front_url": "http://www.test-product-a.fr/product-a.jpg",
                    "categories": "foo",
                    "nutriments": {
                        "energy_value": "1",
                        "energy_unit": "gr",
                        "carbohydrates_100g": "1",
                        "sugars_100g": "1",
                        "fat_100g": "1",
                        "saturated-fat_100g": "1",
                        "salt_100g": "0.1",
                        "sodium_100g": "0.1",
                        "fiber_100g": "0.1",
                        "proteins_100g": "0.1",
                    },
                },
                {
                    "product_name": "ProductB",
                    "nutrition_grade_fr": "b",
                    "url": "http://www.test-product-b.fr",
                    "image_front_url": "http://www.test-product-b.fr/product-b.jpg",
                    "categories": "foo",
                    "nutriments": {
                        "energy_value": "3",
                        "energy_unit": "gr",
                        "carbohydrates_100g": "2",
                        "sugars_100g": "2",
                        "fat_100g": "2",
                        "saturated-fat_100g": "2",
                        "salt_100g": "0.2",
                        "sodium_100g": "0.2",
                        "fiber_100g": "0.2",
                        "proteins_100g": "0.2",
                    },
                },
            ]
        },
        status=200,
    )
    payload = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": "foo",
        "sort_by": "unique_scans_n",
        "page_size": 500,
        "json": 1,
    }
    resp_categories = requests.get("https://fr.openfoodfacts.org/categories.json")
    resp_product = requests.get(
        "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
    )
    command = command_import()
    command.handle()
    assert resp_categories.status_code == 200
    assert resp_product.status_code == 200
    # Test ProductA
    assert Product.objects.filter(name="ProductA").exists()
    assert Product.objects.filter(nutrition_grade="a").exists()
    categ_foo = Category.objects.get(name="foo")
    assert categ_foo in product_a.categories.all()
    # Test ProductB
    assert Product.objects.filter(name="ProductB").exists()
    assert Product.objects.filter(nutrition_grade="b").exists()
    product_b_selected = Product.objects.get(name="ProductB")
    assert categ_foo in product_b_selected.categories.all()
    # Count in database
    assert Product.objects.count() == 2
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_valid_one_category_updated(mocked_responses):
    """Valid if one category can be upadted in database

    Args:
        mocked_responses (fixture): test function was called with mocked_responses
    """
    Category.objects.create(name="pate-a-tartiner")
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={"tags": [{"name": "Pâte-à-Tartiner", "products": 5002}]},
        status=200,
        content_type="application/json",
    )
    resp = requests.get("https://fr.openfoodfacts.org/categories.json")
    command = command_import()
    selected = command.get_populate_categories()
    assert resp.status_code == 200
    assert len(selected) == 1
    assert selected[0]["name"] == "Pâte-à-Tartiner"
    assert selected[0]["products"] == 5002
