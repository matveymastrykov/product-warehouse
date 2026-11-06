# Подключаем функцию для соединения с базой данных.
from database import get_connection

# Подключаем модель позиции списания.
from models import WriteoffItem


# Преобразует строку из SQLite в объект WriteoffItem.
def _map(row) -> WriteoffItem:
    return WriteoffItem(  # Создаём и возвращаем объект позиции списания.
        writeoff_item_id=row[0],  # Берём ID записи из первого столбца строки базы данных.
        writeoff_id=row[1],  # Берём ID списания из второго столбца.
        item_id=row[2],  # Берём ID позиции поставки из третьего столбца.
        quantity=row[3],  # Берём количество списанного продукта из четвёртого столбца.
    )  # Завершаем создание объекта WriteoffItem.


# Возвращает все позиции списаний.
def get_all() -> list[WriteoffItem]:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок, в котором выполняется запрос.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.

        # Получаем записи из таблицы и сортируем по ID.
        cursor.execute(  # Выполняем SQL-запрос для получения всех позиций списания.
            "SELECT writeoff_item_id, writeoff_id, item_id, quantity "  # Выбираем нужные столбцы таблицы.
            "FROM writeoff_items ORDER BY writeoff_item_id"  # Указываем таблицу и сортируем записи по ID.
        )  # Завершаем выполнение SQL-запроса.

        # Преобразуем строки из базы в объекты модели.
        return [_map(row) for row in cursor.fetchall()]  # Получаем все строки и преобразуем каждую в WriteoffItem.
    finally:  # Этот блок выполнится даже в случае ошибки.
        # Закрываем соединение с базой.
        connection.close()  # Освобождаем соединение с базой данных.


# Ищет позицию списания по её ID.
def get_by_id(writeoff_item_id: int) -> WriteoffItem | None:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос для поиска позиции списания.
            "SELECT writeoff_item_id, writeoff_id, item_id, quantity "  # Выбираем поля позиции списания.
            "FROM writeoff_items WHERE writeoff_item_id = ?",  # Ищем запись с указанным ID.
            (writeoff_item_id,),  # Передаём ID отдельно от SQL-запроса как параметр.
        )  # Завершаем выполнение SQL-запроса.
        row = cursor.fetchone()  # Получаем одну найденную строку или None, если записи нет.

        # Возвращаем объект, если запись найдена, иначе None.
        return _map(row) if row else None  # Преобразуем строку в объект модели, если запись существует.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Добавляет позицию списания и возвращает её ID.
def create(writeoff_id: int, item_id: int, quantity: int) -> int:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на добавление позиции списания.
            "INSERT INTO writeoff_items (writeoff_id, item_id, quantity) "  # Указываем таблицу и столбцы для записи.
            "VALUES (?, ?, ?)",  # Указываем три параметра для значений столбцов.
            (writeoff_id, item_id, quantity),  # Передаём ID списания, ID позиции и количество.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем новую запись в базе данных.

        # Возвращаем ID созданной записи.
        return cursor.lastrowid  # Получаем ID последней добавленной записи.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Изменяет данные позиции списания.
def update(
    writeoff_item_id: int,  # ID позиции списания, которую нужно изменить.
    writeoff_id: int,  # Новый или текущий ID списания.
    item_id: int,  # Новый или текущий ID позиции поставки.
    quantity: int,  # Новое количество списанного продукта.
) -> bool:  # Функция возвращает True, если запись была изменена.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на изменение позиции списания.
            "UPDATE writeoff_items "  # Указываем таблицу, в которой нужно изменить запись.
            "SET writeoff_id = ?, item_id = ?, quantity = ? "  # Задаём новые значения полей.
            "WHERE writeoff_item_id = ?",  # Ограничиваем изменение записью с указанным ID.
            (writeoff_id, item_id, quantity, writeoff_item_id),  # Передаём значения в порядке параметров запроса.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем изменения в базе данных.

        # True — запись найдена и обновлена.
        return cursor.rowcount > 0  # Проверяем, изменил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Удаляет позицию списания по её ID.
def delete(writeoff_item_id: int) -> bool:  # Принимаем ID записи и указываем, что вернётся True или False.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на удаление позиции списания.
            "DELETE FROM writeoff_items WHERE writeoff_item_id = ?",  # Удаляем запись с указанным ID.
            (writeoff_item_id,),  # Передаём ID отдельно от SQL-запроса.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем удаление в базе данных.

        # True — запись удалена.
        return cursor.rowcount > 0  # Проверяем, удалил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.