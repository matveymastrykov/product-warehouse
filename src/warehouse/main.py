from pathlib import Path
import sqlite3


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIR / "warehouse.db"
SCHEMA_PATH = PROJECT_DIR / "schema.sql"


def initialize_database():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema)


def show_stock():
    with sqlite3.connect(DATABASE_PATH) as connection:
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
        """).fetchall()

    print("\nОстатки товаров:")
    for product_name, category_name, quantity in rows:
        print(f"{product_name} — {category_name}: {quantity}")


if __name__ == "__main__":
    initialize_database()
    show_stock()