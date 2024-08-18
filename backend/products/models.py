import uuid

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
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


class CustReverseManyToOneDescriptor(ReverseManyToOneDescriptor):
    """Дескриптор, добавление методов: all, generate."""

    def all(self):
        """Проксирует метод all ReverseManyToOne менеджера."""
        return super().all()

    def generate(self):
        """Генерация UniqueProduct (правила генерации могут быть любые)."""
        related_model = self.field.related_model
        instance = self.instance
        unique_product = related_model.objects.create(product=instance)
        return unique_product


class CustForeignKey(ForeignKey):
    """
    ForeignKey является подклассом ForeignObject и нужен для
    установки связи "ManyToOne" между моделями.
    Кастомный ForeignKey, который обеспечивает интерфейс
    взаимодействия Product instance с UniqueProduct instances
    (по сути создаёт дополнительную абстракцию для reverse_many_to_one_manager).
    Использует дескриптор CustReverseManyToOneDescriptor для связи с UniqueProduct.
    """
    #related_accessor_class = ReverseOneToOneDescriptor
    related_accessor_class = CustReverseManyToOneDescriptor

    def __init__(self, *args, **kwargs):
        """Инициализация параметров ForeignKey."""
        super().__init__(*args, **kwargs)


class UniqueProduct(TimeStampedModel):
    """
    Модель уникального продукта.
    CustForeignKey создаёт дополнительную абстракцию
    между Product и UniqueProduct.
    """
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    product = CustForeignKey(
        "Product",
        on_delete=models.PROTECT,
        related_name="unique_products",
        verbose_name="Уникальный продукт"
    )
    attr = models.ForeignKey(
        "ProductAttr",
        on_delete=models.PROTECT,
        related_name="unique_products",
        verbose_name="Уникальный атрибут"
    )

    class Meta:
        verbose_name = "Уникальный продукт"
        verbose_name_plural = "Уникальные продукты"
        ordering = ("created",)

    def __str__(self):
        return f"Уникальный Продукт {self.product} с атрибутом: {self.attr} "