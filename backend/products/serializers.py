from rest_framework import serializers

from products.models import Attr, Product, ProductAttr, UniqueProduct


class AttrSerializer(serializers.ModelSerializer):
    """Сериализатор для модели атрибутов."""

    class Meta:
        model = Attr
        fields = ("id", "name")


class ProductAttrSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели связи атрибутов и продукта."""
    product_name = serializers.CharField(source="product.name", read_only=True)
    attr_name = serializers.CharField(source="attr.name", read_only=True)

    class Meta:
        model = ProductAttr
        fields = ("id", "product_name", "attr_name", "value")


class UniqueProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уникального продукта."""
    product = serializers.CharField(source="product.name", read_only=True)
    attr = ProductAttrSerializer()

    class Meta:
        model = UniqueProduct
        fields = ("id", "product", "attr")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели продукта."""
    user = serializers.SerializerMethodField()
    attrs_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "user", "name", "attrs_name")

    @staticmethod
    def get_user(instance) -> str:
        """Получаем username пользователя."""
        return instance.user.username

    def get_attrs_name(self, obj):
        """Получаем список имён атрибутов."""
        return [attr.name for attr in obj.attrs.all()]
