# Импортируем репозиторий, который работает с таблицей списаний.
from repositories import writeoff_repository

# Импортируем репозиторий для работы с позициями поставок.
from repositories import delivery_item_repository

# Импортируем репозиторий для работы с позициями списаний.
from repositories import writeoff_item_repository

# Импортируем модель списания для аннотации типа возвращаемого значения.
from models import Writeoff


# Возвращаем список всех списаний.
def get_all() -> list[Writeoff]:
    # Запрашиваем список у репозитория и возвращаем его вызывающему коду.
    return writeoff_repository.get_all()


# Ищем списание по его идентификатору.
def get_by_id(writeoff_id: int) -> Writeoff:
    # Просим репозиторий найти списание с указанным ID.
    writeoff = writeoff_repository.get_by_id(writeoff_id)

    # Проверяем, нашлось ли списание.
    if not writeoff:
        # Если списания нет, сообщаем об этом через исключение.
        raise ValueError("Списание не найдено")

    # Возвращаем найденный объект списания.
    return writeoff


# Проверяем данные и создаём документ списания.
def create_writeoff(writeoff_date: str, reason: str) -> int:
    # Удаляем пробелы в начале и конце даты.
    writeoff_date = writeoff_date.strip()

    # Удаляем пробелы в начале и конце причины списания.
    reason = reason.strip()

    # Проверяем, что дата указана.
    if not writeoff_date:
        # Если дата пустая, сообщаем об ошибке.
        raise ValueError("Укажите дату списания")

    # Проверяем, что причина указана.
    if not reason:
        # Если причина пустая, сообщаем об ошибке.
        raise ValueError("Укажите причину списания")

    # Передаём проверенные данные в репозиторий и возвращаем ID нового списания.
    return writeoff_repository.create(writeoff_date, reason)


# Проверяем данные и изменяем существующее списание.
def update_writeoff(
    writeoff_id: int,  # Принимаем ID списания, которое нужно изменить.
    writeoff_date: str,  # Принимаем новую дату списания.
    reason: str,  # Принимаем новую причину списания.
) -> bool:  # Указываем, что функция вернёт True или False.
    # Удаляем пробелы в начале и конце даты.
    writeoff_date = writeoff_date.strip()

    # Удаляем пробелы в начале и конце причины.
    reason = reason.strip()

    # Проверяем, что дата заполнена.
    if not writeoff_date:
        # Если дата пустая, сообщаем об ошибке.
        raise ValueError("Укажите дату списания")

    # Проверяем, что причина заполнена.
    if not reason:
        # Если причина пустая, сообщаем об ошибке.
        raise ValueError("Укажите причину списания")

    # Проверяем, существует ли списание с указанным ID.
    if not writeoff_repository.get_by_id(writeoff_id):
        # Если списания нет, сообщаем об ошибке.
        raise ValueError("Списание не найдено")

    # Передаём проверенные данные в репозиторий и возвращаем результат обновления.
    return writeoff_repository.update(writeoff_id, writeoff_date, reason)


# Удаляем списание по его ID.
def delete_writeoff(writeoff_id: int) -> bool:
    # Проверяем, существует ли списание перед удалением.
    if not writeoff_repository.get_by_id(writeoff_id):
        # Если списания нет, сообщаем об ошибке.
        raise ValueError("Списание не найдено")

    # Удаляем запись через репозиторий и возвращаем результат.
    return writeoff_repository.delete(writeoff_id)


# Считаем, сколько продукта осталось в конкретной позиции поставки.
def get_remaining_quantity(item_id: int) -> int:
    # Ищем позицию поставки по её ID.
    delivery_item = delivery_item_repository.get_by_id(item_id)

    # Проверяем, найдена ли позиция поставки.
    if not delivery_item:
        # Если позиция не найдена, сообщаем об ошибке.
        raise ValueError("Позиция поставки не найдена")

    # Считаем общее количество продукта, уже списанное из этой позиции поставки.
    written_off = sum(
        item.quantity  # Берём количество из текущей записи о списании.
        for item in writeoff_item_repository.get_all()  # Перебираем все позиции списаний.
        if item.item_id == item_id  # Учитываем только записи для нужной позиции поставки.
    )  # Завершаем подсчёт суммы списанного количества.

    # Вычитаем списанное количество из количества, полученного при поставке.
    return delivery_item.quantity - written_off


# Добавляем позицию поставки в документ списания.
def add_writeoff_item(
    writeoff_id: int,  # Принимаем ID документа списания.
    item_id: int,  # Принимаем ID позиции поставки.
    quantity: int,  # Принимаем количество продукта для списания.
) -> int:  # Указываем, что функция вернёт ID созданной записи.
    # Проверяем, существует ли документ списания.
    if not writeoff_repository.get_by_id(writeoff_id):
        # Если документа нет, сообщаем об ошибке.
        raise ValueError("Списание не найдено")

    # Проверяем, что количество больше нуля.
    if quantity <= 0:
        # Если количество нулевое или отрицательное, сообщаем об ошибке.
        raise ValueError("Количество должно быть больше нуля")

    # Проверяем, добавляли ли эту позицию поставки в этот документ раньше.
    already_added = any(
        item.writeoff_id == writeoff_id  # Проверяем, совпадает ли ID документа списания.
        and item.item_id == item_id  # Проверяем, совпадает ли ID позиции поставки.
        for item in writeoff_item_repository.get_all()  # Перебираем все позиции списаний.
    )  # Получаем True, если такая позиция уже добавлена.

    # Проверяем, была ли позиция уже добавлена в этот документ.
    if already_added:
        # Если позиция уже есть, запрещаем добавить её повторно.
        raise ValueError("Эта позиция уже добавлена в списание")

    # Получаем количество продукта, которое ещё осталось в позиции поставки.
    remaining = get_remaining_quantity(item_id)

    # Проверяем, не превышает ли запрошенное количество доступный остаток.
    if quantity > remaining:
        # Если продукта не хватает, сообщаем, сколько доступно для списания.
        raise ValueError(
            f"Недостаточно остатка. Доступно для списания: {remaining}"
        )

    # Если проверки пройдены, создаём запись о позиции списания.
    return writeoff_item_repository.create(
        writeoff_id,  # Передаём ID документа списания.
        item_id,  # Передаём ID позиции поставки.
        quantity,  # Передаём количество продукта для списания.
    )  # Возвращаем ID созданной записи.