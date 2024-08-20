import pytest
from django.test import TestCase
from products.models import Product, ProductAttr, UniqueProduct, Attr
from users.models import CustUser


class UniqueProductTest(TestCase):

    def setUp(self):
        """Настройка начальных данных для тестов."""
        # Создаем пользователя
        self.user = CustUser.objects.create(username="test_pavlen")

        # Создаем продукты
        self.product_1 = Product.objects.create(name="Тест Колбаса докторская", user=self.user)
        self.product_2 = Product.objects.create(name="Тест Помидоры", user=self.user)

        # Создаем атрибуты
        self.attr_taste = Attr.objects.create(name="Вкус")
        self.attr_color = Attr.objects.create(name="Цвет")

        # Создаем промежуточную ProductAttr с ссылками на продукты и атрибуты
        self.product_attr_1 = ProductAttr.objects.create(
            product=self.product_1, attr=self.attr_taste, value="Слабосоленая")
        self.product_attr_2 = ProductAttr.objects.create(
            product=self.product_1, attr=self.attr_color, value="Бордовый")
        self.product_attr_3 = ProductAttr.objects.create(
            product=self.product_2, attr=self.attr_taste, value="Ароматный")
        self.product_attr_4 = ProductAttr.objects.create(
            product=self.product_2, attr=self.attr_color, value="Красный")

        # Создаем уникальные продукты и прицепляем к ним атрибуты
        self.unique_product_1 = UniqueProduct.objects.create(product=self.product_1)
        self.unique_product_1.attrs.add(self.product_attr_1, self.product_attr_2)
        self.unique_product_2 = UniqueProduct.objects.create(product=self.product_2)
        self.unique_product_2.attrs.add(self.product_attr_3, self.product_attr_4)


    def test_all_method(self):
        """Проверка работы метода all()."""

        unique_products_1 = self.product_1.unique_products.all()
        unique_products_2 = self.product_2.unique_products.all()

        # Добавляем различные проверки
        self.assertEqual(len(unique_products_1), 1)
        self.assertEqual(len(unique_products_2), 1)
        self.assertTrue(unique_products_1[0].attrs.filter(attr=self.attr_taste).exists())
        self.assertTrue(unique_products_1[0].attrs.filter(attr=self.attr_color).exists())
        self.assertTrue(unique_products_2[0].attrs.filter(attr=self.attr_taste).exists())
        self.assertTrue(unique_products_2[0].attrs.filter(attr=self.attr_color).exists())

        # Проверка общего количества уникальных продуктов
        total_unique_products = UniqueProduct.objects.count()
        self.assertEqual(total_unique_products, 2)

    def test_generate_method(self):
        """Проверка работы метода generate()."""
        unique_product = UniqueProduct.objects.generate(self.product_1)
        self.assertIsNotNone(unique_product)
        self.assertIsInstance(unique_product, UniqueProduct)
        self.assertEqual(unique_product.product, self.product_1)
        self.assertTrue(UniqueProduct.objects.filter(id=unique_product.id).exists())

    # def test_custom_related_manager(self):
    #     # Получаем имя self.product_1
    #     product = Product.objects.get(name="Тест Колбаса докторская")
    #
    #     # Получаем связанные объекты через кастомный внешний ключ
    #     unique_products = product.unique_products.all()
    #
    #     # Проверяем, что обратное связывание через кастомный внешний ключ
    #     # работает корректно
    #     self.assertEqual(len(unique_products), 1)
    #     self.assertEqual(unique_products[0], self.unique_product_1)