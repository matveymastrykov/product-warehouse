from pathlib import Path  # Подключает инструменты для работы с путями к файлам
import sqlite3  # Подключает модуль для работы с базой SQLite


PROJECT_DIR = Path(__file__).resolve().parent  # Находит папку, в которой лежит этот файл
DATABASE_PATH = PROJECT_DIR / "warehouse.db"  # Указывает путь к файлу базы данных
SCHEMA_PATH = PROJECT_DIR / "schema.sql"  # Указывает путь к файлу со SQL-командами


def initialize_database():  # Объявляет функцию подготовки базы данных
    schema = SCHEMA_PATH.read_text(encoding="utf-8")  # Читает содержимое файла schema.sql

    with sqlite3.connect(DATABASE_PATH) as connection:  # Открывает базу данных или создаёт её
        connection.execute("PRAGMA foreign_keys = ON")  # Включает проверку внешних ключей
        connection.executescript(schema)  # Выполняет SQL-команды из файла schema.sql


def show_stock():  # Объявляет функцию расчёта и вывода остатков
    with sqlite3.connect(DATABASE_PATH) as connection:  # Подключается к базе данных
        # Выполняет запрос: считает поступления и списания каждого продукта
        rows = connection.execute("""
            SELECT
                products.name,
                categories.name,
                COALESCE(deliveries.quantity, 0)
                    - COALESCE(writeoffs.quantity, 0)
            FROM products
            JOIN categories
                ON categories.category_id = products.category_id
            LEFT JOIN (
                SELECT product_id, SUM(quantity) AS quantity
                FROM delivery_items
                GROUP BY product_id
            ) AS deliveries
                ON deliveries.product_id = products.product_id
            LEFT JOIN (
                SELECT delivery_items.product_id, SUM(writeoff_items.quantity) AS quantity
                FROM writeoff_items
                JOIN delivery_items
                    ON delivery_items.item_id = writeoff_items.item_id
                GROUP BY delivery_items.product_id
            ) AS writeoffs
                ON writeoffs.product_id = products.product_id
            ORDER BY products.name
        """).fetchall()  # Получает все строки, найденные запросом

    print("\nОстатки товаров:")  # Выводит заголовок
    for product_name, category_name, quantity in rows:  # Перебирает товары и их остатки
        print(f"{product_name} — {category_name}: {quantity}")  # Печатает название, категорию и остаток


if __name__ == "__main__":  # Проверяет, запущен ли файл напрямую
    initialize_database()  # Подготавливает базу данных
    show_stock()  # Показывает остатки товаров