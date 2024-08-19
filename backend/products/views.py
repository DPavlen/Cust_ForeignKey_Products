from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Product, UniqueProduct
from .serializers import ProductSerializer, UniqueProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"


class UniqueProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet уникальных продуктов."""
    queryset = UniqueProduct.objects.all()
    serializer_class = UniqueProductSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"
