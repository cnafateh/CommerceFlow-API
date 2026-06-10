from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from .filters import ProductFilter
from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name", "brand__name"]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer