import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from products.models import Brand, Category, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    return baker.make(Category, name="Laptop", slug="laptop", is_active=True)


@pytest.fixture
def brand():
    return baker.make(Brand, name="Apple", slug="apple", is_active=True)


@pytest.fixture
def product(category, brand):
    return baker.make(
        Product,
        category=category,
        brand=brand,
        name="MacBook Pro M4",
        slug="macbook-pro-m4",
        price="2499.99",
        is_active=True,
    )


@pytest.mark.django_db
def test_product_list_api_returns_active_products(api_client, product):
    url = reverse("product-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "MacBook Pro M4"


@pytest.mark.django_db
def test_product_detail_api_returns_product_by_slug(api_client, product):
    url = reverse("product-detail", kwargs={"slug": product.slug})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "MacBook Pro M4"
    assert response.data["slug"] == "macbook-pro-m4"


@pytest.mark.django_db
def test_product_list_api_does_not_return_inactive_products(
    api_client,
    category,
    brand,
):
    baker.make(
        Product,
        category=category,
        brand=brand,
        name="Hidden Product",
        slug="hidden-product",
        price="100.00",
        is_active=False,
    )

    url = reverse("product-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_product_filter_by_category(api_client, product):
    url = reverse("product-list")

    response = api_client.get(url, {"category": "laptop"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["slug"] == "macbook-pro-m4"


@pytest.mark.django_db
def test_product_filter_by_brand(api_client, product):
    url = reverse("product-list")

    response = api_client.get(url, {"brand": "apple"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["slug"] == "macbook-pro-m4"


@pytest.mark.django_db
def test_product_search(api_client, product):
    url = reverse("product-list")

    response = api_client.get(url, {"search": "MacBook"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "MacBook Pro M4"