import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from accounts.models import User
from cart.models import Cart, CartItem
from products.models import Brand, Category, Product


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123",
    )


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def product():
    category = baker.make(Category, name="Laptop", slug="laptop", is_active=True)
    brand = baker.make(Brand, name="Apple", slug="apple", is_active=True)
    return baker.make(
        Product,
        category=category,
        brand=brand,
        name="MacBook Pro",
        slug="macbook-pro",
        price="2000.00",
        is_active=True,
    )


@pytest.mark.django_db
def test_authenticated_user_can_view_cart(api_client):
    url = reverse("cart")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["items"] == []


@pytest.mark.django_db
def test_authenticated_user_can_add_item_to_cart(api_client, product):
    url = reverse("cart-item-add")

    response = api_client.post(
        url,
        {
            "product_id": product.id,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["total_items"] == 2
    assert response.data["items"][0]["product"]["id"] == product.id


@pytest.mark.django_db
def test_adding_same_product_increases_quantity(api_client, user, product):
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=1)

    url = reverse("cart-item-add")

    response = api_client.post(
        url,
        {
            "product_id": product.id,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["total_items"] == 3


@pytest.mark.django_db
def test_authenticated_user_can_update_cart_item(api_client, user, product):
    cart = Cart.objects.create(user=user)
    item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    url = reverse("cart-item-update", kwargs={"pk": item.id})

    response = api_client.patch(
        url,
        {
            "quantity": 5,
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["total_items"] == 5


@pytest.mark.django_db
def test_authenticated_user_can_delete_cart_item(api_client, user, product):
    cart = Cart.objects.create(user=user)
    item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    url = reverse("cart-item-delete", kwargs={"pk": item.id})

    response = api_client.delete(url)

    assert response.status_code == 204
    assert CartItem.objects.count() == 0