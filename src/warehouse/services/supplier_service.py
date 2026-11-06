import sqlite3  # Импортируем тип ошибки, возникающей при нарушении ограничений SQLite
# Импортируем репозиторий для работы с поставщиками.
from repositories import supplier_repository

# Импортируем модель поставщика для аннотации типа.
from models import Supplier


# Объявляем функцию, которая возвращает список всех поставщиков.
def get_all() -> list[Supplier]:
    # Получаем список поставщиков из репозитория и возвращаем его.
    return supplier_repository.get_all()


# Объявляем функцию поиска поставщика по ID.
def get_by_id(supplier_id: int) -> Supplier:
    # Получаем поставщика с указанным ID из репозитория.
    supplier = supplier_repository.get_by_id(supplier_id)

    # Проверяем, найден ли поставщик.
    if not supplier:
        # Если поставщик не найден, сообщаем об ошибке.
        raise ValueError("Поставщик не найден")

    # Возвращаем найденного поставщика.
    return supplier


# Проверяем данные и добавляем нового поставщика.
def create_supplier(name: str, phone: str | None = None) -> int:
    # Убираем пробелы в начале и конце названия поставщика.
    name = name.strip()

    # Если телефон указан, убираем пробелы по краям; если нет — сохраняем None.
    phone = phone.strip() if phone else None

    # Проверяем, что название поставщика не пустое.
    if not name:
        # Если название пустое, сообщаем об ошибке.
        raise ValueError("Название поставщика не может быть пустым")

    # Перебираем список всех поставщиков, чтобы найти совпадение по названию.
    for supplier in supplier_repository.get_all():
        # Сравниваем названия без учёта регистра букв.
        if supplier.name.lower() == name.lower():
            # Если поставщик с таким названием уже есть, сообщаем об ошибке.
            raise ValueError("Поставщик с таким названием уже существует")

    # Создаём поставщика через репозиторий и возвращаем ID новой записи.
    return supplier_repository.create(name, phone)


# Проверяем данные и изменяем существующего поставщика.
def update_supplier(
    supplier_id: int,  # ID поставщика, которого нужно изменить.
    name: str,  # Новое название поставщика.
    phone: str | None = None,  # Новый телефон или None, если он не указан.
) -> bool:  # Функция возвращает True или False в зависимости от результата.
    # Убираем пробелы в начале и конце названия поставщика.
    name = name.strip()

    # Если телефон указан, убираем пробелы по краям; если нет — сохраняем None.
    phone = phone.strip() if phone else None

    # Проверяем, что название поставщика не пустое.
    if not name:
        # Если название пустое, сообщаем об ошибке.
        raise ValueError("Название поставщика не может быть пустым")

    # Проверяем, существует ли поставщик с указанным ID.
    if not supplier_repository.get_by_id(supplier_id):
        # Если поставщик не найден, сообщаем об ошибке.
        raise ValueError("Поставщик не найден")

    # Перебираем всех поставщиков, чтобы проверить уникальность нового названия.
    for supplier in supplier_repository.get_all():
        # Проверяем, что это другой поставщик и его название совпадает с новым.
        if (
            supplier.supplier_id != supplier_id
            and supplier.name.lower() == name.lower()
        ):
            # Если название занято другим поставщиком, сообщаем об ошибке.
            raise ValueError("Поставщик с таким названием уже существует")

    # Передаём новые данные в репозиторий и возвращаем результат обновления.
    return supplier_repository.update(supplier_id, name, phone)


def delete_supplier(supplier_id: int) -> bool:  # Удаляем поставщика, если он существует и не связан с поставками.
    if not supplier_repository.get_by_id(supplier_id):  # Проверяем, существует ли поставщик.
        raise ValueError("Поставщик не найден")  # Сообщаем, если поставщика с таким ID нет.
    try:  # Начинаем обработку возможного запрета на удаление.
        return supplier_repository.delete(supplier_id)  # Просим репозиторий удалить поставщика.
    except sqlite3.IntegrityError as error:  # Перехватываем нарушение внешнего ключа.
        raise ValueError("Нельзя удалить поставщика, у которого есть поставки") from error  # Показываем понятную ошибку.