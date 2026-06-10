from django.urls import path

from .views import PaymentAPIView

urlpatterns = [
    path(
        "<int:order_id>/",
        PaymentAPIView.as_view(),
        name="payment",
    ),
]