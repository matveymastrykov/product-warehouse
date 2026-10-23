from pathlib import Path  # Подключает инструменты для работы с путями к файлам
import sqlite3  # Подключает модуль для работы с базой данных SQLite


PROJECT_DIR = Path(__file__).resolve().parent  # Находит папку, в которой лежит этот Python-файл
DATABASE_PATH = PROJECT_DIR / "warehouse.db"  # Формирует путь к файлу базы данных
SCHEMA_PATH = PROJECT_DIR / "schema.sql"  # Формирует путь к SQL-файлу со структурой базы данных


def initialize_database():  # Объявляет функцию подготовки базы данных
    schema = SCHEMA_PATH.read_text(encoding="utf-8")  # Читает содержимое schema.sql в текстовую переменную

    with sqlite3.connect(DATABASE_PATH) as connection:  # Открывает базу или создаёт её, если файла ещё нет
        connection.execute("PRAGMA foreign_keys = ON")  # Включает проверку внешних ключей для этого соединения
        connection.executescript(schema)  # Выполняет SQL-команды из файла schema.sql


def show_stock():  # Объявляет функцию расчёта и вывода складских остатков
    with sqlite3.connect(DATABASE_PATH) as connection:  # Подключается к базе данных
        rows = connection.execute("""  # Выполняет SQL-запрос и начинает многострочный текст запроса
            SELECT  -- Указывает, какие данные нужно получить
                products.name,  -- Выбирает название продукта
                categories.name,  -- Выбирает название категории продукта
                COALESCE(deliveries.quantity, 0)  -- Берёт сумму поступлений; если её нет, подставляет 0
                    - COALESCE(writeoffs.quantity, 0)  -- Вычитает сумму списаний; если их нет, подставляет 0
            FROM products  -- Начинает выборку с таблицы продуктов
            JOIN categories  -- Присоединяет таблицу категорий
                ON categories.category_id = products.category_id  -- Связывает продукт с его категорией по ID
            LEFT JOIN (  -- Присоединяет данные о поступлениях, сохраняя продукты без поступлений
                SELECT product_id, SUM(quantity) AS quantity  -- Считает общее количество поступившего каждого продукта
                FROM delivery_items  -- Берёт позиции поставок
                GROUP BY product_id  -- Группирует позиции по продуктам
            ) AS deliveries  -- Даёт результату подзапроса имя deliveries
                ON deliveries.product_id = products.product_id  -- Связывает суммы поступлений с продуктами
            LEFT JOIN (  -- Присоединяет данные о списаниях, сохраняя продукты без списаний
                SELECT delivery_items.product_id, SUM(writeoff_items.quantity) AS quantity  -- Считает списания по продуктам
                FROM writeoff_items  -- Берёт позиции списаний
                JOIN delivery_items  -- Присоединяет позиции поставок, к которым относятся списания
                    ON delivery_items.item_id = writeoff_items.item_id  -- Связывает списание с позицией поставки
                GROUP BY delivery_items.product_id  -- Группирует списания по продуктам
            ) AS writeoffs  -- Даёт результату подзапроса имя writeoffs
                ON writeoffs.product_id = products.product_id  -- Связывает суммы списаний с продуктами
            ORDER BY products.name  -- Сортирует результат по названию продукта
        """).fetchall()  # Завершает SQL-запрос и получает все найденные строки

    print("\nОстатки товаров:")  # Печатает заголовок списка остатков
    for product_name, category_name, quantity in rows:  # Перебирает строки: название, категория и остаток
        print(f"{product_name} — {category_name}: {quantity}")  # Выводит информацию о продукте и его остатке


if __name__ == "__main__":  # Проверяет, запущен ли этот файл напрямую
    initialize_database()  # Подготавливает базу данных
    show_stock()  # Рассчитывает и выводит остатки товаров