import pytest
from products.models import Product, UniqueProduct, UniqueProductManager
from users.models import CustUser


@pytest.fixture
def user():
    """Создание тестового пользователя."""
    return CustUser.objects.create(username="test_user")


@pytest.fixture
def product(user):
    """Создание тестового продукта."""
    return Product.objects.create(name="Тестовый продукт", user=user)


@pytest.fixture
def product_with_unique(product):
    """Создание продукта с уникальным продуктом."""
    unique = UniqueProduct.objects.create(product=product)
    return product, unique


@pytest.mark.django_db
class TestCustForeignKey:
    """Тесты кастомного ForeignKey с related_accessor_class."""

    def test_custom_manager_type(self, product):
        """Проверка, что product.unique_products возвращает кастомный менеджер."""
        manager = product.unique_products

        print(f"\nТип менеджера: {type(manager).__name__}")
        print(f"Модуль: {type(manager).__module__}")

        assert isinstance(manager, UniqueProductManager), (
            f"Ожидается UniqueProductManager, получен {type(manager)}"
        )

    def test_all_method_proxy(self, product_with_unique):
        """Проверка, что метод all() проксирует стандартный менеджер."""
        product, unique = product_with_unique

        unique_products = product.unique_products.all()

        print(f"\nВызов: product.unique_products.all()")
        print(f"Результат: {list(unique_products)}")
        print(f"Количество: {len(unique_products)}")

        assert len(unique_products) == 1
        assert unique_products[0] == unique
        assert unique_products[0].product == product

    def test_generate_method_creates_unique_product(self, product):
        """Проверка, что метод generate() создаёт UniqueProduct."""
        initial_count = product.unique_products.all().count()

        new_unique = product.unique_products.generate()

        print(f"\nВызов: product.unique_products.generate()")
        print(f"Создан: {new_unique}")
        print(f"ID: {new_unique.id}")
        print(f"Количество до: {initial_count}, после: {product.unique_products.all().count()}")

        assert isinstance(new_unique, UniqueProduct)
        assert new_unique.product == product
        assert product.unique_products.all().count() == initial_count + 1
        assert UniqueProduct.objects.filter(id=new_unique.id).exists()

    def test_multiple_products_isolation(self, user):
        """Проверка изоляции UniqueProduct между разными Product."""
        product_1 = Product.objects.create(name="Продукт 1", user=user)
        product_2 = Product.objects.create(name="Продукт 2", user=user)

        unique_1 = product_1.unique_products.generate()
        unique_2 = product_2.unique_products.generate()

        product_1_uniques = list(product_1.unique_products.all())
        product_2_uniques = list(product_2.unique_products.all())

        print(f"\nProduct 1 содержит {len(product_1_uniques)} UniqueProduct")
        print(f"Product 2 содержит {len(product_2_uniques)} UniqueProduct")

        assert len(product_1_uniques) == 1
        assert len(product_2_uniques) == 1
        assert unique_1 in product_1_uniques
        assert unique_2 in product_2_uniques
        assert unique_1 not in product_2_uniques
        assert unique_2 not in product_1_uniques

    def test_custom_interface_has_required_methods(self, product):
        """Проверка наличия методов all() и generate() в кастомном интерфейсе."""
        manager = product.unique_products

        print(f"\nМетод all(): {hasattr(manager, 'all')}")
        print(f"Метод generate(): {hasattr(manager, 'generate')}")

        assert hasattr(manager, "all"), "Метод all() отсутствует"
        assert hasattr(manager, "generate"), "Метод generate() отсутствует"
        assert callable(manager.all), "Метод all() не вызываемый"
        assert callable(manager.generate), "Метод generate() не вызываемый"