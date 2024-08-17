from django.contrib import admin

from products.models import Attr, Product, ProductAttr


@admin.register(Attr)
class AttrAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления атрибутами.
    """
    list_display = ("id", "name",)
    search_fields = ("id", "name",)
    list_filter = ("id", "name",)
    list_editable = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления продуктами.
    """
    def get_attrs(self, obj):
        return " ; ".join([attr.name for attr in obj.attrs.all()])

    get_attrs.short_description = "Attributes"

    list_display = ("id", "name", "get_attrs")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    list_editable = ("name",)
    empty_value_display = "-пусто-"


@admin.register(ProductAttr)
class ProductAttrAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления связи атрибутов и продукта.
    """
    list_display = ("id", "attr", "product", "value")
    search_fields = ("id", "attr", "product", "value")
    list_filter = ("id", "attr", "product", "value")
    # list_editable = ("name",)
    empty_value_display = "-пусто-"
