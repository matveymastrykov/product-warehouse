# Импортируем репозитории для работы с категориями и продуктами.
from repositories import category_repository, product_repository

# Импортируем модель продукта для аннотации типов.
from models import Product


# Объявляем функцию, которая возвращает все продукты.
def get_all() -> list[Product]:
    # Получаем список продуктов из репозитория и возвращаем его.
    return product_repository.get_all()


# Объявляем функцию проверки данных и создания продукта.
def create_product(name: str, unit: str, category_id: int) -> int:
    # Убираем пробелы в начале и конце названия продукта.
    name = name.strip()

    # Убираем пробелы в начале и конце единицы измерения.
    unit = unit.strip()

    # Проверяем, что название продукта не пустое.
    if not name:
        # Если название пустое, сообщаем об ошибке.
        raise ValueError("Название продукта не может быть пустым")

    # Проверяем, что единица измерения указана.
    if not unit:
        # Если единица измерения не указана, сообщаем об ошибке.
        raise ValueError("Укажите единицу измерения")

    # Проверяем, существует ли категория с указанным ID.
    if not category_repository.get_by_id(category_id):
        # Если категория не найдена, сообщаем об ошибке.
        raise ValueError("Категория не найдена")

    # Передаём проверенные данные в репозиторий и возвращаем ID нового продукта.
    return product_repository.create(name, unit, category_id)


# Объявляем функцию изменения продукта, если он существует и данные корректны.
def update_product(
    product_id: int,  # ID продукта, который нужно изменить.
    name: str,  # Новое название продукта.
    unit: str,  # Новая единица измерения.
    category_id: int,  # ID категории для продукта.
) -> bool:  # Функция возвращает True или False в зависимости от результата.
    # Убираем пробелы в начале и конце названия продукта.
    name = name.strip()

    # Убираем пробелы в начале и конце единицы измерения.
    unit = unit.strip()

    # Проверяем, что название продукта не пустое.
    if not name:
        # Если название пустое, сообщаем об ошибке.
        raise ValueError("Название продукта не может быть пустым")

    # Проверяем, что единица измерения указана.
    if not unit:
        # Если единица измерения не указана, сообщаем об ошибке.
        raise ValueError("Укажите единицу измерения")

    # Проверяем, существует ли продукт с указанным ID.
    if not product_repository.get_by_id(product_id):
        # Если продукт не найден, сообщаем об ошибке.
        raise ValueError("Продукт не найден")

    # Проверяем, существует ли категория с указанным ID.
    if not category_repository.get_by_id(category_id):
        # Если категория не найдена, сообщаем об ошибке.
        raise ValueError("Категория не найдена")

    # Передаём проверенные данные в репозиторий и возвращаем результат обновления.
    return product_repository.update(product_id, name, unit, category_id)


# Ищем продукт по ID и сообщаем об ошибке, если его нет.
def get_by_id(product_id: int) -> Product:
    # Запрашиваем продукт с указанным ID из репозитория.
    product = product_repository.get_by_id(product_id)

    # Проверяем, найден ли продукт.
    if not product:
        # Если продукт не найден, сообщаем об ошибке.
        raise ValueError("Продукт не найден")

    # Возвращаем найденный продукт.
    return product


# Удаляем продукт, если он существует.
def delete_product(product_id: int) -> bool:
    # Проверяем, существует ли продукт перед удалением.
    if not product_repository.get_by_id(product_id):
        # Если продукт не найден, сообщаем об ошибке.
        raise ValueError("Продукт не найден")

    # Передаём удаление репозиторию и возвращаем результат операции.
    return product_repository.delete(product_id)