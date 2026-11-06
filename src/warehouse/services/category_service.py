# Подключаем репозиторий для работы с категориями.
from repositories import category_repository

# Подключаем модель категории.
from models import Category


# Объявляем функцию, которая возвращает список всех категорий.
def get_all() -> list[Category]:
    # Получаем список категорий из репозитория и возвращаем его.
    return category_repository.get_all()


# Объявляем функцию поиска категории по её ID.
def get_by_id(category_id: int) -> Category:
    # Получаем категорию с указанным ID из репозитория.
    category = category_repository.get_by_id(category_id)

    # Проверяем, найдена ли категория.
    if not category:
        # Если категория не найдена, вызываем ошибку с пояснением.
        raise ValueError("Категория не найдена")

    # Возвращаем найденную категорию.
    return category


# Объявляем функцию проверки названия и создания новой категории.
def create_category(name: str) -> int:
    # Убираем пробелы в начале и конце названия.
    name = name.strip()

    # Проверяем, что после удаления пробелов название не пустое.
    if not name:
        # Если название пустое, вызываем ошибку.
        raise ValueError("Название категории не может быть пустым")

    # Получаем список всех категорий для проверки на дубликаты.
    categories = category_repository.get_all()

    # Перебираем категории из полученного списка.
    for category in categories:
        # Сравниваем названия без учёта регистра букв.
        if category.name.lower() == name.lower():
            # Если категория с таким названием уже есть, вызываем ошибку.
            raise ValueError("Категория с таким названием уже существует")

    # Создаём категорию через репозиторий и возвращаем её ID.
    return category_repository.create(name)


# Объявляем функцию проверки данных и изменения категории.
def update_category(category_id: int, name: str) -> bool:
    # Убираем пробелы в начале и конце нового названия.
    name = name.strip()

    # Проверяем, что новое название не пустое.
    if not name:
        # Если название пустое, вызываем ошибку.
        raise ValueError("Название категории не может быть пустым")

    # Проверяем, существует ли категория, которую нужно изменить.
    if not category_repository.get_by_id(category_id):
        # Если категория не найдена, вызываем ошибку.
        raise ValueError("Категория не найдена")

    # Получаем список категорий, чтобы проверить, не занято ли новое название.
    categories = category_repository.get_all()

    # Перебираем все категории.
    for category in categories:
        # Проверяем, что это другая категория и её название совпадает с новым.
        if (
            category.category_id != category_id
            and category.name.lower() == name.lower()
        ):
            # Если название уже используется другой категорией, вызываем ошибку.
            raise ValueError("Категория с таким названием уже существует")

    # Передаём ID категории и новое название в репозиторий для обновления.
    return category_repository.update(category_id, name)


# Объявляем функцию удаления категории по ID.
def delete_category(category_id: int) -> bool:
    # Проверяем, существует ли категория перед удалением.
    if not category_repository.get_by_id(category_id):
        # Если категория не найдена, вызываем ошибку.
        raise ValueError("Категория не найдена")

    # Просим репозиторий удалить категорию и возвращаем результат операции.
    return category_repository.delete(category_id)