from pathlib import Path  # Инструменты для работы с путями
import sqlite3  # Модуль для работы с SQLite
from contextlib import contextmanager  # Помогает безопасно управлять подключением


PROJECT_DIR = Path(__file__).resolve().parent  # Папка, где лежит database.py
DATABASE_PATH = PROJECT_DIR / "warehouse.db"  # Путь к файлу базы данных
SCHEMA_PATH = PROJECT_DIR / "schema.sql"  # Путь к файлу со схемой базы данных


@contextmanager  # Позволяет использовать подключение через with
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)  # Открывает базу данных
    connection.row_factory = sqlite3.Row  # Позволяет получать значения столбцов по имени
    connection.execute("PRAGMA foreign_keys = ON")  # Включает проверку внешних ключей

    try:
        yield connection  # Передаёт подключение коду, который его использует
        connection.commit()  # Сохраняет изменения после успешной работы
    except Exception:
        connection.rollback()  # Отменяет изменения, если произошла ошибка
        raise  # Передаёт ошибку дальше
    finally:
        connection.close()  # Закрывает подключение


def initialize_database():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")  # Читает команды из schema.sql

    with get_connection() as connection:  # Открывает подключение к базе
        connection.executescript(schema)  # Выполняет SQL-команды из файла