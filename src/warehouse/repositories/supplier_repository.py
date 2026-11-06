from database import get_connection  # Импортируем контекстный менеджер подключения к базе данных.
from models import Supplier  # Импортируем модель поставщика.


def _map(row) -> Supplier:  # Преобразуем строку базы данных в объект модели Supplier.
    return Supplier(  # Создаём объект поставщика.
        supplier_id=row[0],  # Берём ID поставщика из первого столбца.
        name=row[1],  # Берём название поставщика из второго столбца.
        phone=row[2],  # Берём телефон поставщика из третьего столбца.
    )  # Завершаем создание объекта Supplier.


def get_all() -> list[Supplier]:  # Получаем список всех поставщиков.
    with get_connection() as connection:  # Открываем подключение, которое закроется после выхода из блока.
        rows = connection.execute(  # Выполняем запрос и получаем строки поставщиков.
            "SELECT supplier_id, name, phone FROM suppliers ORDER BY supplier_id"  # Выбираем поля и сортируем по ID.
        ).fetchall()  # Получаем все строки результата.
    return [_map(row) for row in rows]  # Преобразуем строки в объекты Supplier и возвращаем список.


def get_by_id(supplier_id: int) -> Supplier | None:  # Ищем поставщика по ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        row = connection.execute(  # Выполняем запрос для поиска поставщика.
            "SELECT supplier_id, name, phone FROM suppliers WHERE supplier_id = ?",  # Ищем запись с указанным ID.
            (supplier_id,),  # Передаём ID параметром отдельно от SQL-запроса.
        ).fetchone()  # Получаем одну строку или None.
    return _map(row) if row else None  # Возвращаем модель поставщика или None, если его нет.


def create(name: str, phone: str | None = None) -> int:  # Добавляем поставщика и возвращаем его ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на добавление поставщика.
            "INSERT INTO suppliers (name, phone) VALUES (?, ?)",  # Добавляем название и телефон через параметры.
            (name, phone),  # Передаём значения в порядке столбцов.
        )  # Завершаем выполнение запроса.
        supplier_id = cursor.lastrowid  # Получаем ID только что добавленного поставщика.
    return supplier_id  # Возвращаем ID после завершения транзакции.


def update(supplier_id: int, name: str, phone: str | None = None) -> bool:  # Изменяем данные поставщика.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на обновление данных.
            "UPDATE suppliers SET name = ?, phone = ? WHERE supplier_id = ?",  # Меняем название и телефон по ID.
            (name, phone, supplier_id),  # Передаём новое название, телефон и ID.
        )  # Завершаем выполнение запроса.
        updated = cursor.rowcount > 0  # Проверяем, была ли найдена и изменена запись.
    return updated  # Возвращаем True, если поставщик обновлён.


def delete(supplier_id: int) -> bool:  # Удаляем поставщика по ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на удаление поставщика.
            "DELETE FROM suppliers WHERE supplier_id = ?",  # Удаляем запись с указанным ID.
            (supplier_id,),  # Передаём ID параметром.
        )  # Завершаем выполнение запроса.
        deleted = cursor.rowcount > 0  # Проверяем, была ли найдена и удалена запись.
    return deleted  # Возвращаем True, если поставщик удалён.