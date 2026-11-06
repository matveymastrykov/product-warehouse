# Подключаем функцию для соединения с базой данных.
from database import get_connection

# Подключаем модель списания.
from models import Writeoff


# Преобразует строку из SQLite в объект Writeoff.
def _map(row) -> Writeoff:
    return Writeoff(  # Создаём объект списания и возвращаем его.
        writeoff_id=row[0],  # Берём ID списания из первого столбца строки.
        writeoff_date=row[1],  # Берём дату списания из второго столбца.
        reason=row[2],  # Берём причину списания из третьего столбца.
    )  # Завершаем создание объекта Writeoff.


# Возвращает список всех списаний.
def get_all() -> list[Writeoff]:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.

        # Получаем списания и сортируем по дате — сначала последние.
        cursor.execute(  # Выполняем запрос для получения всех списаний.
            "SELECT writeoff_id, writeoff_date, reason "  # Выбираем ID, дату и причину списания.
            "FROM writeoffs ORDER BY writeoff_date DESC"  # Берём записи из таблицы и сортируем по убыванию даты.
        )  # Завершаем выполнение SQL-запроса.

        # Преобразуем строки из базы в объекты Writeoff.
        return [_map(row) for row in cursor.fetchall()]  # Получаем все строки, преобразуем их и возвращаем список.
    finally:  # Этот блок выполнится даже в случае ошибки.
        # Закрываем соединение даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Ищет списание по ID.
def get_by_id(writeoff_id: int) -> Writeoff | None:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос для поиска списания по ID.
            "SELECT writeoff_id, writeoff_date, reason "  # Выбираем ID, дату и причину списания.
            "FROM writeoffs WHERE writeoff_id = ?",  # Ищем запись с указанным ID.
            (writeoff_id,),  # Передаём ID отдельно от SQL-запроса как параметр.
        )  # Завершаем выполнение SQL-запроса.
        row = cursor.fetchone()  # Получаем одну найденную строку или None, если записи нет.

        # Возвращаем объект, если списание найдено, иначе None.
        return _map(row) if row else None  # Преобразуем найденную строку в объект Writeoff.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Добавляет новое списание и возвращает его ID.
def create(writeoff_date: str, reason: str) -> int:
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на добавление списания.
            "INSERT INTO writeoffs (writeoff_date, reason) "  # Указываем таблицу и столбцы для новой записи.
            "VALUES (?, ?)",  # Указываем два параметра для значений столбцов.
            (writeoff_date, reason),  # Передаём дату и причину в соответствующем порядке.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем новую запись в базе данных.

        # Возвращаем ID созданного списания.
        return cursor.lastrowid  # Получаем ID последней добавленной записи.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Изменяет дату и причину списания.
def update(
    writeoff_id: int,  # ID списания, которое нужно изменить.
    writeoff_date: str,  # Новая дата списания.
    reason: str,  # Новая причина списания.
) -> bool:  # Функция возвращает True или False в зависимости от результата.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на изменение списания.
            "UPDATE writeoffs "  # Указываем таблицу, в которой изменяем запись.
            "SET writeoff_date = ?, reason = ? "  # Задаём новые значения даты и причины.
            "WHERE writeoff_id = ?",  # Ограничиваем изменение записью с указанным ID.
            (writeoff_date, reason, writeoff_id),  # Передаём новую дату, причину и ID в порядке параметров.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем изменения в базе данных.

        # True — запись найдена и изменена, False — такого ID нет.
        return cursor.rowcount > 0  # Проверяем, изменил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.


# Удаляет списание по ID.
def delete(writeoff_id: int) -> bool:  # Принимаем ID списания и указываем тип результата.
    connection = get_connection()  # Открываем соединение с базой данных.
    try:  # Начинаем блок выполнения запроса.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-команд.
        cursor.execute(  # Выполняем запрос на удаление списания.
            "DELETE FROM writeoffs WHERE writeoff_id = ?",  # Удаляем запись с указанным ID.
            (writeoff_id,),  # Передаём ID отдельно от SQL-запроса.
        )  # Завершаем выполнение SQL-запроса.
        connection.commit()  # Сохраняем удаление в базе данных.

        # True — запись удалена.
        return cursor.rowcount > 0  # Проверяем, удалил ли запрос хотя бы одну строку.
    finally:  # Этот блок выполнится даже в случае ошибки.
        connection.close()  # Закрываем соединение с базой данных.