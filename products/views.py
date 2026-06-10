from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer