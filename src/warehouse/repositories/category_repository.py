from database import get_connection  # Импортируем контекстный менеджер подключения к базе данных.
from models import Category  # Импортируем модель категории.


def _map(row) -> Category:  # Преобразуем строку базы данных в объект модели Category.
    return Category(  # Создаём объект категории.
        category_id=row[0],  # Берём ID категории из первого столбца.
        name=row[1],  # Берём название категории из второго столбца.
    )  # Завершаем создание объекта Category.


def get_all() -> list[Category]:  # Получаем список всех категорий.
    with get_connection() as connection:  # Открываем подключение и автоматически закрываем его после работы.
        rows = connection.execute(  # Выполняем запрос и получаем все найденные строки.
            "SELECT category_id, name FROM categories ORDER BY category_id"  # Выбираем ID и название категорий.
        ).fetchall()  # Получаем результаты запроса.
    return [_map(row) for row in rows]  # Преобразуем строки базы в объекты Category и возвращаем список.


def get_by_id(category_id: int) -> Category | None:  # Ищем категорию по ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        row = connection.execute(  # Выполняем запрос для поиска одной категории.
            "SELECT category_id, name FROM categories WHERE category_id = ?",  # Ищем категорию с указанным ID.
            (category_id,),  # Передаём ID параметром, отдельно от SQL-запроса.
        ).fetchone()  # Получаем одну строку или None, если категория не найдена.
    return _map(row) if row else None  # Возвращаем объект категории или None.


def create(name: str) -> int:  # Добавляем категорию и возвращаем её ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на добавление категории.
            "INSERT INTO categories (name) VALUES (?)",  # Добавляем название через параметр.
            (name,),  # Передаём название отдельно от SQL-запроса.
        )  # Завершаем выполнение запроса.
        category_id = cursor.lastrowid  # Сохраняем ID созданной категории.
    return category_id  # Возвращаем ID после завершения работы с подключением.


def update(category_id: int, name: str) -> bool:  # Изменяем название категории по её ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на изменение категории.
            "UPDATE categories SET name = ? WHERE category_id = ?",  # Задаём новое название для категории с указанным ID.
            (name, category_id),  # Передаём новое название и ID параметрами.
        )  # Завершаем выполнение запроса.
        updated = cursor.rowcount > 0  # Проверяем, была ли найдена и изменена категория.
    return updated  # Возвращаем True, если категория изменена, иначе False.


def delete(category_id: int) -> bool:  # Удаляем категорию по её ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на удаление категории.
            "DELETE FROM categories WHERE category_id = ?",  # Удаляем категорию с указанным ID.
            (category_id,),  # Передаём ID параметром.
        )  # Завершаем выполнение запроса.
        deleted = cursor.rowcount > 0  # Проверяем, была ли найдена и удалена категория.
    return deleted  # Возвращаем True, если категория удалена, иначе False.