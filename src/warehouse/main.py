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
                COALESCE(SUM(delivery_items.quantity), 0)
            FROM products
            JOIN categories USING (category_id)
            LEFT JOIN delivery_items USING (product_id)
            GROUP BY products.product_id
            ORDER BY products.name
        """).fetchall()

    print("\nОстатки товаров:")
    for product_name, category_name, quantity in rows:
        print(f"{product_name} — {category_name}: {quantity}")


if __name__ == "__main__":
    initialize_database()
    show_stock()