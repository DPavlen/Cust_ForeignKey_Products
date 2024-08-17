from django.db import models


class Attr(models.Model):
    """Модель атрибутов."""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта."""
    name = models.CharField(max_length=100)
    attrs = models.ManyToManyField("Attr", through="ProductAttr")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class ProductAttr(models.Model):
    """Промежуточная Модель связи атрибутов и продукта ."""
    attr = models.ForeignKey("Attr", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Атрибут и Продукт"
        verbose_name_plural = "Атрибуты и Продукты"

    def __str__(self):
        return (f"Продукт {self.product} с атрибутами: {self.attr}"
                f" значениями: {self.value} ")

# class UniqueProduct(models.Model):
#     """Модель уникального продукта."""
#     product = models.CustomForeignKey(Product, on_delete=models.PROTECT)
#     attr = models.ForeignKey(ProductAttr, on_delete=models.PROTECT)
