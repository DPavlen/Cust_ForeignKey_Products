from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Product, UniqueProduct
from .schemas import PRODUCTS_VIEWSET_SCHEMA, UNIQUE_PRODUCT_VIEWSET_SCHEMA
from .serializers import ProductSerializer, UniqueProductSerializer


@extend_schema_view(**PRODUCTS_VIEWSET_SCHEMA)
class ProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"


@extend_schema_view(**UNIQUE_PRODUCT_VIEWSET_SCHEMA)
class UniqueProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet уникальных продуктов."""
    queryset = UniqueProduct.objects.all()
    serializer_class = UniqueProductSerializer
    permission_classes = (AllowAny,)
    lookup_field = "pk"
