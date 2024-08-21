import uuid
import logging
#
# from products.manager import UniqueProductManager, CustForeignKey

logger = logging.getLogger("django")

from django.db import models
from django.db.models.fields.related import ForeignKey
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


class CustForeignKey(ForeignKey):
    """
    Кастомный внешний ключ для установки связи "ManyToOne" между моделями.
    Обеспечивает использование кастомного менеджера для обратных связей.
    """

    def contribute_to_related_class(self, cls, related):
        """Настройка класса модели для использования кастомного менеджера
        при обращении к обратной связи."""
        super().contribute_to_related_class(cls, related)
        setattr(cls, self.name, UniqueProductManager())


class UniqueProductManager(models.Manager):
    """Кастомный менеджер для модели UniqueProduct."""

    def all(self):
        """Переопределяет метод all() для использования кастомного менеджера."""
        return super().all()

    def generate(self, instance):
        """Создает уникальный продукт на основе переданного экземпляра."""
        return self.create(product=instance)


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
    attrs = models.ManyToManyField(
        "ProductAttr",
        related_name="unique_products",
        verbose_name="Атрибуты уникального продукта"
    )
    objects = UniqueProductManager()

    class Meta:
        verbose_name = "Уникальный продукт"
        verbose_name_plural = "Уникальные продукты"
        ordering = ("created",)

    def __str__(self):
        return f"Уникальный Продукт {self.product}"