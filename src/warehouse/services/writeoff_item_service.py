# Подключаем репозитории документов списания, позиций поставки и позиций списания.
from repositories import (
    writeoff_repository,
    delivery_item_repository,
    writeoff_item_repository,
)

# Подключаем модель позиции списания.
from models import WriteoffItem


# Возвращаем список всех позиций списания.
def get_all() -> list[WriteoffItem]:
    # Получаем данные из репозитория и возвращаем их.
    return writeoff_item_repository.get_all()


# Ищем позицию списания по её ID.
def get_by_id(writeoff_item_id: int) -> WriteoffItem:
    # Запрашиваем позицию списания в репозитории.
    writeoff_item = writeoff_item_repository.get_by_id(writeoff_item_id)

    # Проверяем, найдена ли позиция.
    if not writeoff_item:
        # Если позиции нет, сообщаем об ошибке.
        raise ValueError("Позиция списания не найдена")

    # Возвращаем найденную позицию.
    return writeoff_item


# Считаем, сколько продукта осталось в позиции поставки.
def get_remaining_quantity(item_id: int) -> int:
    # Ищем позицию поставки по её ID.
    delivery_item = delivery_item_repository.get_by_id(item_id)

    # Проверяем, существует ли такая позиция поставки.
    if not delivery_item:
        # Если позиции нет, сообщаем об ошибке.
        raise ValueError("Позиция поставки не найдена")

    # Суммируем количество продукта, уже списанное из этой позиции поставки.
    written_off = sum(
        item.quantity  # Берём количество из текущей позиции списания.
        for item in writeoff_item_repository.get_all()  # Перебираем все позиции списаний.
        if item.item_id == item_id  # Учитываем только записи для нужной позиции поставки.
    )  # Завершаем подсчёт общего количества списанного продукта.

    # Вычитаем уже списанное количество из количества в поставке.
    return delivery_item.quantity - written_off


# Проверяем данные и добавляем позицию в документ списания.
def create_writeoff_item(
    writeoff_id: int,  # ID документа списания.
    item_id: int,  # ID позиции поставки.
    quantity: int,  # Количество продукта для списания.
) -> int:  # Функция возвращает ID новой позиции списания.
    # Проверяем, существует ли документ списания.
    if not writeoff_repository.get_by_id(writeoff_id):
        # Если документа нет, сообщаем об ошибке.
        raise ValueError("Списание не найдено")

    # Проверяем, существует ли позиция поставки.
    if not delivery_item_repository.get_by_id(item_id):
        # Если позиции поставки нет, сообщаем об ошибке.
        raise ValueError("Позиция поставки не найдена")

    # Проверяем, что количество для списания больше нуля.
    if quantity <= 0:
        # Если количество нулевое или отрицательное, сообщаем об ошибке.
        raise ValueError("Количество должно быть больше нуля")

    # Проверяем, не добавлена ли эта позиция поставки в документ раньше.
    for item in writeoff_item_repository.get_all():
        # Сравниваем ID документа и ID позиции поставки.
        if item.writeoff_id == writeoff_id and item.item_id == item_id:
            # Если такая позиция уже есть, запрещаем добавить её повторно.
            raise ValueError("Эта позиция уже добавлена в списание")

    # Получаем остаток продукта в позиции поставки.
    remaining = get_remaining_quantity(item_id)

    # Проверяем, хватает ли остатка для списания указанного количества.
    if quantity > remaining:
        # Если остатка недостаточно, сообщаем доступное количество.
        raise ValueError(
            f"Недостаточно остатка. Доступно для списания: {remaining}"
        )

    # Создаём позицию списания через репозиторий и возвращаем её ID.
    return writeoff_item_repository.create(writeoff_id, item_id, quantity)


# Проверяем данные и изменяем существующую позицию списания.
def update_writeoff_item(
    writeoff_item_id: int,  # ID позиции списания, которую нужно изменить.
    writeoff_id: int,  # ID документа списания.
    item_id: int,  # ID позиции поставки.
    quantity: int,  # Новое количество продукта для списания.
) -> bool:  # Функция возвращает True, если запись обновлена.
    # Получаем существующую позицию или вызываем ошибку, если её нет.
    old_item = get_by_id(writeoff_item_id)

    # Проверяем, существует ли документ, к которому будет относиться позиция.
    if not writeoff_repository.get_by_id(writeoff_id):
        # Если документа нет, сообщаем об ошибке.
        raise ValueError("Списание не найдено")

    # Проверяем, существует ли выбранная позиция поставки.
    if not delivery_item_repository.get_by_id(item_id):
        # Если позиции поставки нет, сообщаем об ошибке.
        raise ValueError("Позиция поставки не найдена")

    # Проверяем, что новое количество больше нуля.
    if quantity <= 0:
        # Если количество нулевое или отрицательное, сообщаем об ошибке.
        raise ValueError("Количество должно быть больше нуля")

    # Перебираем позиции списания, чтобы найти возможный дубликат.
    for item in writeoff_item_repository.get_all():
        # Проверяем совпадение документа и позиции, исключая редактируемую запись.
        if (
            item.writeoff_item_id != writeoff_item_id
            and item.writeoff_id == writeoff_id
            and item.item_id == item_id
        ):
            # Если такая другая запись уже существует, сообщаем об ошибке.
            raise ValueError("Эта позиция уже добавлена в списание")

    # Получаем остаток продукта с учётом всех текущих списаний.
    remaining = get_remaining_quantity(item_id)

    # Если оставляем ту же позицию поставки, возвращаем её старое количество в доступный остаток.
    if old_item.item_id == item_id:
        # Добавляем прежнее количество, потому что при проверке оно считается уже списанным.
        remaining += old_item.quantity

    # Проверяем, хватает ли остатка для нового количества.
    if quantity > remaining:
        # Если остатка недостаточно, сообщаем доступное количество.
        raise ValueError(
            f"Недостаточно остатка. Доступно для списания: {remaining}"
        )

    # Передаём обновлённые данные в репозиторий и возвращаем результат.
    return writeoff_item_repository.update(
        writeoff_item_id,  # Передаём ID изменяемой позиции списания.
        writeoff_id,  # Передаём ID документа списания.
        item_id,  # Передаём ID позиции поставки.
        quantity,  # Передаём новое количество продукта.
    )  # Завершаем вызов репозитория.


# Удаляем позицию списания по её ID.
def delete_writeoff_item(writeoff_item_id: int) -> bool:
    # Проверяем, существует ли позиция перед удалением.
    get_by_id(writeoff_item_id)

    # Удаляем позицию через репозиторий и возвращаем результат.
    return writeoff_item_repository.delete(writeoff_item_id)