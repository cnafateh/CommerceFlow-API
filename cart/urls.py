from django.urls import path

from .views import (
    AddCartItemAPIView,
    CartAPIView,
    DeleteCartItemAPIView,
    UpdateCartItemAPIView,
)

urlpatterns = [
    path("", CartAPIView.as_view(), name="cart"),
    path(
        "items/",
        AddCartItemAPIView.as_view(),
        name="cart-item-add",
    ),
    path(
        "items/<int:pk>/",
        UpdateCartItemAPIView.as_view(),
        name="cart-item-update",
    ),
    path(
        "items/<int:pk>/delete/",
        DeleteCartItemAPIView.as_view(),
        name="cart-item-delete",
    ),
]