import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from accounts.models import User
from cart.models import Cart, CartItem
from orders.models import Order, OrderStatus
from payments.models import Payment
from products.models import Brand, Category, Product


@pytest.fixture
def user():
    return User.objects.create_user(
        username="buyer",
        email="buyer@example.com",
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
def test_checkout_creates_order_and_clears_cart(api_client, user, product):
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=2)

    url = reverse("checkout")

    response = api_client.post(url)

    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert response.data["status"] == OrderStatus.PENDING
    assert response.data["total_price"] == "4000.00"
    assert CartItem.objects.count() == 0


@pytest.mark.django_db
def test_checkout_fails_when_cart_is_empty(api_client, user):
    Cart.objects.create(user=user)

    url = reverse("checkout")

    response = api_client.post(url)

    assert response.status_code == 400
    assert response.data["detail"] == "Cart is empty."


@pytest.mark.django_db
def test_payment_creates_payment_and_marks_order_paid(api_client, user, product):
    order = baker.make(Order, user=user, status=OrderStatus.PENDING)

    order.items.create(
        product=product,
        price=product.price,
        quantity=2,
    )

    url = reverse("payment", kwargs={"order_id": order.id})

    response = api_client.post(url)

    order.refresh_from_db()

    assert response.status_code == 201
    assert Payment.objects.count() == 1
    assert order.status == OrderStatus.PAID
    assert response.data["status"] == "SUCCESS"


@pytest.mark.django_db
def test_payment_cannot_be_created_twice(api_client, user, product):
    order = baker.make(Order, user=user, status=OrderStatus.PENDING)

    order.items.create(
        product=product,
        price=product.price,
        quantity=1,
    )

    url = reverse("payment", kwargs={"order_id": order.id})

    first_response = api_client.post(url)
    second_response = api_client.post(url)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.data["detail"] == "Payment already exists."