from rest_framework import viewsets
from .models import Product, UniqueProduct
from .serializers import ProductSerializer, UniqueProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UniqueProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet уникальных продуктов."""
    queryset = UniqueProduct.objects.all()
    serializer_class = UniqueProductSerializer
