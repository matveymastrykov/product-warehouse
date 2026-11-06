from datetime import date  # Импортируем тип даты для проверки формата дат.
from repositories import delivery_repository, supplier_repository  # Импортируем репозитории поставок и поставщиков.
from services import product_service  # Импортируем сервис продуктов для проверки позиций.


def get_all():  # Возвращает список всех поставок.
    return delivery_repository.get_all()  # Получаем поставки через репозиторий.


def get_all_with_items() -> list[tuple]:  # Возвращает поставки вместе с их позициями.
    return delivery_repository.get_all_with_items()  # Получаем поставки и позиции через репозиторий.


def get_by_id(delivery_id: int):  # Ищет поставку по ID.
    delivery = delivery_repository.get_by_id(delivery_id)  # Получаем поставку из репозитория.
    if not delivery:  # Проверяем, найдена ли поставка.
        raise ValueError("Поставка не найдена")  # Сообщаем об ошибке, если запись отсутствует.
    return delivery  # Возвращаем найденную поставку.


def create_delivery(  # Проверяет данные и создаёт поставку вместе с позициями.
    supplier_id: int,  # Принимаем ID поставщика.
    delivery_date: str,  # Принимаем дату поставки.
    items: list[tuple[int, int, float, str]],  # Принимаем позиции: ID продукта, количество, цену и срок годности.
) -> int:  # Возвращаем ID созданной поставки.
    delivery_date = delivery_date.strip()  # Убираем пробелы по краям даты.
    if not delivery_date:  # Проверяем, что дата указана.
        raise ValueError("Укажите дату поставки")  # Сообщаем об отсутствии даты.
    try:  # Начинаем проверку формата даты поставки.
        date.fromisoformat(delivery_date)  # Проверяем формат ГГГГ-ММ-ДД.
    except ValueError as error:  # Перехватываем дату неверного формата.
        raise ValueError("Дата поставки должна быть в формате ГГГГ-ММ-ДД") from error  # Сообщаем ожидаемый формат.

    if not supplier_repository.get_by_id(supplier_id):  # Проверяем существование поставщика.
        raise ValueError("Поставщик не найден")  # Останавливаем создание, если поставщик отсутствует.
    if not items:  # Проверяем, что в поставке есть хотя бы одна позиция.
        raise ValueError("Добавьте хотя бы один продукт")  # Не разрешаем создать пустую поставку.

    products = product_service.get_all()  # Получаем список продуктов через сервис.
    product_ids = {product.product_id for product in products}  # Собираем ID существующих продуктов.
    used_product_ids = set()  # Подготавливаем множество для обнаружения повторов.
    checked_items = []  # Создаём список проверенных позиций.

    for product_id, quantity, unit_price, expiration_date in items:  # Проверяем каждую позицию поставки.
        if product_id not in product_ids:  # Проверяем, существует ли указанный продукт.
            raise ValueError(f"Продукт с ID {product_id} не найден")  # Сообщаем, если продукт отсутствует.
        if product_id in used_product_ids:  # Проверяем, не добавлен ли продукт повторно.
            raise ValueError("Один продукт нельзя добавить дважды в одну поставку")  # Сообщаем о повторе продукта.
        if quantity <= 0:  # Проверяем, что количество положительное.
            raise ValueError("Количество должно быть больше нуля")  # Сообщаем об ошибочном количестве.
        if unit_price < 0:  # Проверяем, что цена не отрицательная.
            raise ValueError("Цена не может быть отрицательной")  # Сообщаем об ошибочной цене.
        try:  # Начинаем проверку срока годности.
            date.fromisoformat(expiration_date.strip())  # Проверяем формат срока годности.
        except ValueError as error:  # Перехватываем срок годности неверного формата.
            raise ValueError("Срок годности должен быть в формате ГГГГ-ММ-ДД") from error  # Сообщаем ожидаемый формат.
        used_product_ids.add(product_id)  # Запоминаем ID проверенного продукта.
        checked_items.append((product_id, quantity, unit_price, expiration_date.strip()))  # Добавляем проверенную позицию.

    return delivery_repository.create(supplier_id, delivery_date, checked_items)  # Сохраняем поставку и её позиции.


def update_delivery(  # Проверяет данные и изменяет поставку.
    delivery_id: int,  # Принимаем ID изменяемой поставки.
    supplier_id: int,  # Принимаем ID поставщика.
    delivery_date: str,  # Принимаем новую дату поставки.
) -> bool:  # Возвращаем результат изменения.
    delivery_date = delivery_date.strip()  # Убираем пробелы по краям даты.
    if not delivery_date:  # Проверяем, что дата указана.
        raise ValueError("Укажите дату поставки")  # Сообщаем об отсутствии даты.
    try:  # Начинаем проверку формата даты.
        date.fromisoformat(delivery_date)  # Проверяем формат ГГГГ-ММ-ДД.
    except ValueError as error:  # Перехватываем дату неверного формата.
        raise ValueError("Дата поставки должна быть в формате ГГГГ-ММ-ДД") from error  # Сообщаем ожидаемый формат.
    if not delivery_repository.get_by_id(delivery_id):  # Проверяем существование поставки.
        raise ValueError("Поставка не найдена")  # Сообщаем, если поставка отсутствует.
    if not supplier_repository.get_by_id(supplier_id):  # Проверяем существование нового поставщика.
        raise ValueError("Поставщик не найден")  # Сообщаем, если поставщик отсутствует.
    return delivery_repository.update(delivery_id, supplier_id, delivery_date)  # Передаём изменение репозиторию.


def delete_delivery(delivery_id: int) -> bool:  # Удаляет поставку, если она существует.
    if not delivery_repository.get_by_id(delivery_id):  # Проверяем наличие поставки.
        raise ValueError("Поставка не найдена")  # Сообщаем, если поставка отсутствует.
    return delivery_repository.delete(delivery_id)  # Передаём удаление репозиторию.