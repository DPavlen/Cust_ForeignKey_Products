from django.contrib import admin

from products.models import Attr, Product, ProductAttr, UniqueProduct


class BaseAdminSettings(admin.ModelAdmin):
    """
    Базовая настройка панели администратора.
    """
    search_fields = ("id", "name", "created")
    list_filter = ("id", "name", "created")
    list_editable = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Attr)
class AttrAdmin(BaseAdminSettings):
    """
    Административный интерфейс для управления атрибутами.
    """
    list_display = ("id", "name", "created", "modified")


@admin.register(Product)
class ProductAdmin(BaseAdminSettings):
    """
    Административный интерфейс для управления продуктами.
    """
    def get_attrs(self, obj):
        """Получаем имена атрибутов."""
        return " ; ".join([attr.name for attr in obj.attrs.all()])
    get_attrs.short_description = "Атрибуты у продукта"

    list_display = ("id", "user", "name", "get_attrs", "created")


@admin.register(ProductAttr)
class ProductAttrAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления связи атрибутов и продукта.
    """
    list_display = ("id", "product", "attr", "value", "created")
    search_fields = ("id", "product", "attr", "value", "created")
    list_filter = ("id", "product", "attr", "value", "created")
    empty_value_display = "-пусто-"


@admin.register(UniqueProduct)
class UniqueProductAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления уникальными продуктами.
    """
    def get_attrs(self, obj):
        """Получаем ManyToManyField из связанной ProductAttr."""
        return " ; ".join([product_attr.value for product_attr in
                           ProductAttr.objects.filter(product=obj.product)])

    get_attrs.short_description = "Уникальные атрибуты продукта"

    list_display = ("id", "product", "get_attrs")
    search_fields = ("id", "product__name")
    list_filter = ("product", "attrs")
    empty_value_display = "-пусто-"