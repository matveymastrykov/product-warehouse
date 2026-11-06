# Подключаем функцию для соединения с базой данных.
from database import get_connection

# Подключаем модель позиции поставки.
from models import DeliveryItem


# Преобразует строку из SQLite в объект DeliveryItem.
def _map(row) -> DeliveryItem:
    return DeliveryItem(  # Создаём и возвращаем объект позиции поставки.
        item_id=row[0],  # Берём ID позиции из первого столбца строки базы данных.
        delivery_id=row[1],  # Берём ID поставки из второго столбца.
        product_id=row[2],  # Берём ID продукта из третьего столбца.
        quantity=row[3],  # Берём количество продукта из четвёртого столбца.
        unit_price=row[4],  # Берём цену одной единицы из пятого столбца.
        expiration_date=row[5],  # Берём срок годности из шестого столбца.
    )  # Завершаем создание объекта DeliveryItem.


# Возвращает все позиции поставок.
def get_all() -> list[DeliveryItem]:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок, в котором выполняем запрос к базе.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос для получения всех позиций поставок.
            "SELECT item_id, delivery_id, product_id, quantity, "  # Выбираем основные поля позиции поставки.
            "unit_price, expiration_date "  # Продолжаем список выбираемых полей.
            "FROM delivery_items ORDER BY item_id"  # Указываем таблицу и сортируем записи по ID.
        )  # Завершаем выполнение SQL-запроса.

        # Преобразуем каждую строку из базы в объект DeliveryItem.
        return [_map(row) for row in cursor.fetchall()]  # Получаем все строки, преобразуем их и возвращаем список.
    finally:  # Этот блок выполнится даже в случае ошибки.
        # Закрываем соединение, чтобы освободить ресурсы.
        connection.close()  # Завершаем соединение с базой данных.


# Ищет позицию поставки по ID.
def get_by_id(item_id: int) -> DeliveryItem | None:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос для поиска позиции по ID.
            "SELECT item_id, delivery_id, product_id, quantity, "  # Выбираем основные поля позиции поставки.
            "unit_price, expiration_date "  # Продолжаем список выбираемых полей.
            "FROM delivery_items WHERE item_id = ?",  # Ищем запись с указанным ID.
            (item_id,),  # Передаём ID отдельно от SQL-запроса как безопасный параметр.
        )  # Завершаем выполнение SQL-запроса.
        row = cursor.fetchone()  # Получаем одну найденную строку или None, если запись отсутствует.

        # Возвращаем найденную позицию или None, если её нет.
        return _map(row) if row else None  # Преобразуем строку в объект, если она найдена.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Добавляет позицию поставки и возвращает её ID.
def create(
    delivery_id: int,  # ID поставки, к которой относится позиция.
    product_id: int,  # ID продукта в этой позиции.
    quantity: int,  # Количество продукта.
    unit_price: float,  # Цена одной единицы продукта.
    expiration_date: str,  # Срок годности продукта.
) -> int:  # Функция возвращает ID созданной записи.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на добавление позиции поставки.
            "INSERT INTO delivery_items "  # Указываем, что добавляем запись в таблицу delivery_items.
            "(delivery_id, product_id, quantity, unit_price, expiration_date) "  # Перечисляем столбцы для заполнения.
            "VALUES (?, ?, ?, ?, ?)",  # Указываем пять параметров для значений этих столбцов.
            (delivery_id, product_id, quantity, unit_price, expiration_date),  # Передаём значения в том же порядке.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем добавленную запись в базе данных.

        # Возвращаем ID добавленной записи.
        return cursor.lastrowid  # Получаем ID последней созданной записи.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Изменяет данные позиции поставки.
def update(
    item_id: int,  # ID позиции, которую нужно изменить.
    delivery_id: int,  # Новый или текущий ID поставки.
    product_id: int,  # Новый или текущий ID продукта.
    quantity: int,  # Новое количество продукта.
    unit_price: float,  # Новая цена одной единицы.
    expiration_date: str,  # Новый срок годности.
) -> bool:  # Функция возвращает True, если запись была изменена.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на изменение позиции поставки.
            "UPDATE delivery_items "  # Указываем таблицу, в которой нужно изменить запись.
            "SET delivery_id = ?, product_id = ?, quantity = ?, "  # Задаём новые значения первых трёх полей.
            "unit_price = ?, expiration_date = ? "  # Задаём новые значения цены и срока годности.
            "WHERE item_id = ?",  # Ограничиваем изменение позицией с указанным ID.
            (  # Начинаем кортеж значений для параметров запроса.
                delivery_id,  # Передаём значение для столбца delivery_id.
                product_id,  # Передаём значение для столбца product_id.
                quantity,  # Передаём значение для столбца quantity.
                unit_price,  # Передаём значение для столбца unit_price.
                expiration_date,  # Передаём значение для столбца expiration_date.
                item_id,  # Передаём ID позиции для условия WHERE.
            ),  # Завершаем кортеж параметров.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем изменения в базе данных.

        # Возвращаем True, если запись найдена и обновлена.
        return cursor.rowcount > 0  # Проверяем, изменил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Удаляет позицию поставки по ID.
def delete(item_id: int) -> bool:  # Функция принимает ID позиции и возвращает результат удаления.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на удаление позиции поставки.
            "DELETE FROM delivery_items WHERE item_id = ?",  # Удаляем запись с указанным ID.
            (item_id,),  # Передаём ID отдельно от SQL-запроса.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем удаление в базе данных.

        # Возвращаем True, если запись была удалена.
        return cursor.rowcount > 0  # Проверяем, удалил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.