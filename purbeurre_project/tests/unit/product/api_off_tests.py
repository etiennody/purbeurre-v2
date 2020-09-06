import json

import pytest
import requests
import responses


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_valid_status_code_api_off_for_categories_is_success(mocked_responses):
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
    mocked_responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        body="{}",
        status=200,
        content_type="application/json",
    )
    resp = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?")
    assert resp.status_code == 200


@responses.activate
def test_valid_api_off_json_category():
    responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/categories.json",
        json={"categorie": "test"},
    )
    resp = requests.get("https://fr.openfoodfacts.org/categories.json")
    assert resp.json() == {"categorie": "test"}


@responses.activate
def test_valid__api_off_json_product():
    responses.add(
        responses.GET,
        "https://fr.openfoodfacts.org/cgi/search.pl?",
        json={
            "product_name": "test",
            "nutrition_grade_fr": "a",
            "url": "http://test.fr",
            "image_front_url": "http://test.fr/test.jpg",
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
        },
    )

    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": "category_test",
        "sort_by": "unique_scans_n",
        "page_size": 500,
        "json": 1,
    }
    resp = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=params)
    assert resp.json() == {
        "product_name": "test",
        "nutrition_grade_fr": "a",
        "url": "http://test.fr",
        "image_front_url": "http://test.fr/test.jpg",
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
    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url
        == "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=category_test&sort_by=unique_scans_n&page_size=500&json=1"
    )
