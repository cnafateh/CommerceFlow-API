from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddCartItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data["product_id"],
            is_active=True,
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": serializer.validated_data["quantity"],
            },
        )

        if not created:
            item.quantity += serializer.validated_data["quantity"]
            item.save()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_201_CREATED,
        )


class UpdateCartItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=pk, cart=cart)

        item.quantity = serializer.validated_data["quantity"]
        item.save()

        return Response(CartSerializer(cart).data)


class DeleteCartItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=pk, cart=cart)

        item.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )