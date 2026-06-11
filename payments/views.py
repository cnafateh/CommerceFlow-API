import uuid

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderStatus

from .models import Payment, PaymentStatus


class PaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
        )

        if hasattr(order, "payment"):
            return Response(
                {"detail": "Payment already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            status=PaymentStatus.SUCCESS,
            transaction_id=str(uuid.uuid4()),
        )

        order.status = OrderStatus.PAID
        order.save(update_fields=["status"])

        return Response(
            {
                "payment_id": payment.id,
                "transaction_id": payment.transaction_id,
                "status": payment.status,
            },
            status=status.HTTP_201_CREATED,
        )