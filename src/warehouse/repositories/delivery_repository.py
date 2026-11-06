from database import get_connection  # Импортируем контекстный менеджер подключения к базе данных.
from models import Delivery  # Импортируем модель поставки.


def _map(row) -> Delivery:  # Преобразуем строку SQLite в объект Delivery.
    return Delivery(  # Создаём объект поставки.
        delivery_id=row[0],  # Записываем ID поставки.
        supplier_id=row[1],  # Записываем ID поставщика.
        delivery_date=row[2],  # Записываем дату поставки.
    )  # Возвращаем созданный объект.


def get_all() -> list[Delivery]:  # Получаем все поставки.
    with get_connection() as connection:  # Открываем соединение через контекстный менеджер.
        rows = connection.execute(  # Выполняем SQL-запрос на получение поставок.
            "SELECT delivery_id, supplier_id, delivery_date "  # Выбираем поля поставки.
            "FROM deliveries ORDER BY delivery_id"  # Берём данные из таблицы и сортируем по ID.
        ).fetchall()  # Получаем все строки результата.
        return [_map(row) for row in rows]  # Преобразуем строки в объекты Delivery.


def get_by_id(delivery_id: int) -> Delivery | None:  # Ищем поставку по ID.
    with get_connection() as connection:  # Открываем соединение через контекстный менеджер.
        row = connection.execute(  # Выполняем запрос на поиск поставки.
            "SELECT delivery_id, supplier_id, delivery_date "  # Выбираем поля поставки.
            "FROM deliveries WHERE delivery_id = ?",  # Ищем запись с указанным ID.
            (delivery_id,),  # Передаём ID отдельно от SQL-запроса.
        ).fetchone()  # Получаем одну строку или None.
        return _map(row) if row else None  # Возвращаем объект либо None, если поставка не найдена.


def create(  # Создаём поставку и, если переданы позиции, добавляем их.
    supplier_id: int,  # ID поставщика.
    delivery_date: str,  # Дата поставки.
    items: list[tuple[int, int, float, str]] | None = None,  # Позиции: ID продукта, количество, цена, срок годности.
) -> int:  # Возвращаем ID созданной поставки.
    with get_connection() as connection:  # Открываем соединение; контекст сохранит изменения при успехе.
        cursor = connection.execute(  # Добавляем запись о поставке.
            "INSERT INTO deliveries (supplier_id, delivery_date) VALUES (?, ?)",  # SQL добавления поставки.
            (supplier_id, delivery_date),  # Передаём ID поставщика и дату.
        )  # Завершаем добавление поставки.
        delivery_id = cursor.lastrowid  # Получаем ID новой поставки.

        if items:  # Проверяем, переданы ли позиции поставки.
            connection.executemany(  # Добавляем все позиции одним вызовом.
                "INSERT INTO delivery_items "  # Указываем таблицу позиций поставки.
                "(delivery_id, product_id, quantity, unit_price, expiration_date) "  # Перечисляем поля таблицы.
                "VALUES (?, ?, ?, ?, ?)",  # Используем параметры для значений.
                [  # Формируем список параметров для каждой позиции.
                    (delivery_id, product_id, quantity, unit_price, expiration_date)  # Добавляем ID поставки к позиции.
                    for product_id, quantity, unit_price, expiration_date in items  # Перебираем переданные позиции.
                ],  # Завершаем список параметров.
            )  # Завершаем добавление позиций.

        return delivery_id  # Возвращаем ID созданной поставки.


def update(  # Изменяем поставщика и дату поставки.
    delivery_id: int,  # ID изменяемой поставки.
    supplier_id: int,  # Новый ID поставщика.
    delivery_date: str,  # Новая дата поставки.
) -> bool:  # Возвращаем True, если запись была найдена.
    with get_connection() as connection:  # Открываем соединение через контекстный менеджер.
        cursor = connection.execute(  # Выполняем запрос на изменение поставки.
            "UPDATE deliveries SET supplier_id = ?, delivery_date = ? "  # Обновляем поставщика и дату.
            "WHERE delivery_id = ?",  # Ограничиваем изменение нужной записью.
            (supplier_id, delivery_date, delivery_id),  # Передаём значения для запроса.
        )  # Завершаем запрос.
        return cursor.rowcount > 0  # Проверяем, была ли найдена и изменена запись.


def delete(delivery_id: int) -> bool:  # Удаляем поступление и связанные с ним позиции.
    with get_connection() as connection:  # Открываем соединение с базой данных.
        delivery = connection.execute(  # Проверяем, существует ли поступление.
            "SELECT delivery_id FROM deliveries WHERE delivery_id = ?",  # Ищем поступление по ID.
            (delivery_id,),  # Передаём ID параметром.
        ).fetchone()  # Получаем строку или None.
        if delivery is None:  # Проверяем, найдено ли поступление.
            return False  # Возвращаем False, если такого поступления нет.
        connection.execute(  # Удаляем связанные позиции поступления.
            "DELETE FROM delivery_items WHERE delivery_id = ?",  # Выбираем позиции по ID поступления.
            (delivery_id,),  # Передаём ID поступления.
        )  # Завершаем удаление позиций.
        cursor = connection.execute(  # Удаляем запись о самом поступлении.
            "DELETE FROM deliveries WHERE delivery_id = ?",  # Выбираем поступление для удаления.
            (delivery_id,),  # Передаём ID поступления.
        )  # Завершаем удаление записи.
        return cursor.rowcount > 0  # Возвращаем True, если поступление удалено.


def get_all_with_items() -> list[tuple]:  # Получаем поставки вместе с данными их позиций.
    with get_connection() as connection:  # Открываем соединение через контекстный менеджер.
        rows = connection.execute(  # Выполняем запрос, объединяющий поставки, позиции и продукты.
            "SELECT deliveries.delivery_id, suppliers.name, deliveries.delivery_date, "  # Выбираем ID, поставщика и дату.
            "products.name, delivery_items.quantity, delivery_items.unit_price, "  # Выбираем продукт, количество и цену.
            "delivery_items.expiration_date "  # Выбираем срок годности.
            "FROM deliveries "  # Начинаем запрос с таблицы поставок.
            "JOIN suppliers ON suppliers.supplier_id = deliveries.supplier_id "  # Находим название поставщика.
            "JOIN delivery_items ON delivery_items.delivery_id = deliveries.delivery_id "  # Находим позиции поставки.
            "JOIN products ON products.product_id = delivery_items.product_id "  # Находим название продукта.
            "ORDER BY deliveries.delivery_date DESC, deliveries.delivery_id DESC"  # Сортируем от новых поставок к старым.
        ).fetchall()  # Получаем все найденные строки.
        return [tuple(row) for row in rows]  # Возвращаем данные как список кортежей.