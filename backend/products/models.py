import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from users.models import CustUser


class Attr(TimeStampedModel):
    """Модель атрибутов."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        "Название атрибута",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ("created",)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """Модель продукта."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        CustUser,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Пользователь"
    )
    name = models.CharField(
        "Название продукта",
        max_length=100,
        unique=True,
    )
    attrs = models.ManyToManyField(
        "Attr",
        through="ProductAttr",
        related_name="products",
        verbose_name="Атрибуты продукта"

    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("created",)

    def __str__(self):
        return self.name


class ProductAttr(TimeStampedModel):
    """Промежуточная Модель связи атрибутов и продукта ."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="product_attrs",
        verbose_name="Продукт"

    )
    attr = models.ForeignKey(
        "Attr",
        on_delete=models.CASCADE,
        related_name="products_attr",
        verbose_name="Атрибут"
    )
    value = models.CharField(
        "Значение у атрибута продукта",
        max_length=100
    )

    class Meta:
        verbose_name = "Продукт и Атрибут"
        verbose_name_plural = "Продукты и Атрибуты"
        ordering = ("created",)

    def __str__(self):
        return (f"Продукт {self.product} с атрибутом: {self.attr} "
                f"имеет значение:  {self.value}")

# class UniqueProduct(models.Model):
#     """Модель уникального продукта."""
#     product = models.CustomForeignKey(Product, on_delete=models.PROTECT)
#     attr = models.ForeignKey(ProductAttr, on_delete=models.PROTECT)
