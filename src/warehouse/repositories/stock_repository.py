from database import get_connection  # Импортируем функцию подключения к базе данных.
from models import Stock  # Импортируем модель остатка из файла models.py.


def get_stock() -> list[Stock]:  # Объявляем функцию, которая возвращает список моделей Stock.
    with get_connection() as connection:  # Открываем соединение с базой данных.
        rows = connection.execute(  # Выполняем запрос, который считает остатки продуктов.
            "SELECT products.name, categories.name, "  # Выбираем названия продукта и категории.
            "COALESCE(deliveries.quantity, 0) - "  # Берём количество поступлений, либо ноль.
            "COALESCE(writeoffs.quantity, 0) "  # Вычитаем количество списаний, либо ноль.
            "FROM products "  # Начинаем выборку из таблицы продуктов.
            "JOIN categories ON categories.category_id = products.category_id "  # Получаем категорию продукта.
            "LEFT JOIN ( "  # Начинаем подзапрос с суммой поступлений.
            "SELECT product_id, SUM(quantity) AS quantity "  # Суммируем поступления по продуктам.
            "FROM delivery_items GROUP BY product_id "  # Группируем позиции поставок по продуктам.
            ") AS deliveries ON deliveries.product_id = products.product_id "  # Связываем поступления с продуктами.
            "LEFT JOIN ( "  # Начинаем подзапрос с суммой списаний.
            "SELECT delivery_items.product_id, SUM(writeoff_items.quantity) AS quantity "  # Суммируем списания по продуктам.
            "FROM writeoff_items "  # Берём позиции списания.
            "JOIN delivery_items ON delivery_items.item_id = writeoff_items.item_id "  # Находим продукт для каждого списания.
            "GROUP BY delivery_items.product_id "  # Группируем списания по продуктам.
            ") AS writeoffs ON writeoffs.product_id = products.product_id "  # Связываем списания с продуктами.
            "ORDER BY products.name"  # Сортируем продукты по названию.
        ).fetchall()  # Получаем найденные строки из базы данных.

    return [Stock(*row) for row in rows]  # Преобразуем каждую строку базы в объект модели Stock.