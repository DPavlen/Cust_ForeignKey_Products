import uuid
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
from model_utils.models import TimeStampedModel

User = get_user_model()
logger = logging.getLogger("django")


class Attr(TimeStampedModel):
    """Атрибут продукта (например: Цвет, Вкус)."""
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
    """Продукт с набором атрибутов."""
    id = models.UUIDField(
        "id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Пользователь",
        null=True,
        blank=True,
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
    """Связь продукта с атрибутом и его значением."""
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


class UniqueProductManager:
    """Кастомный интерфейс обратной связи Product -> UniqueProduct."""

    def __init__(self, related_manager):
        """Оборачивает стандартный ReverseManyToOne менеджер."""
        self._related_manager = related_manager

    def all(self):
        """Возвращает все UniqueProduct для данного Product."""
        return self._related_manager.all()

    def generate(self):
        """Создаёт новый UniqueProduct для данного Product."""
        return self._related_manager.create()


class CustReverseManyToOneDescriptor(ReverseManyToOneDescriptor):
    """Дескриптор обратной связи с кастомным интерфейсом."""

    def __get__(self, instance, cls=None):
        """Возвращает UniqueProductManager вместо стандартного менеджера."""
        if instance is None:
            return self
        related_manager = super().__get__(instance, cls)
        return UniqueProductManager(related_manager)


class CustForeignKey(ForeignKey):
    """ForeignKey с кастомным интерфейсом обратной связи через related_accessor_class."""
    related_accessor_class = CustReverseManyToOneDescriptor


class UniqueProduct(TimeStampedModel):
    """Уникальный продукт с конкретными значениями атрибутов."""
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
    #attr = models.ForeignKey(ProductAttr, on_delete=models.PROTECT)
    attrs = models.ManyToManyField(
        "ProductAttr",
        related_name="unique_products",
        verbose_name="Атрибуты уникального продукта"
    )

    class Meta:
        verbose_name = "Уникальный продукт"
        verbose_name_plural = "Уникальные продукты"
        ordering = ("created",)

    def __str__(self):
        return f"Уникальный Продукт {self.product}"