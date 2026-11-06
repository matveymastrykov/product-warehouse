from database import get_connection  # Импортируем контекстный менеджер подключения к базе данных.
from models import Product  # Импортируем модель продукта.


def _map(row) -> Product:  # Объявляем функцию преобразования строки базы в модель Product.
    return Product(  # Создаём и возвращаем объект продукта.
        product_id=row[0],  # Записываем ID продукта.
        name=row[1],  # Записываем название продукта.
        unit=row[2],  # Записываем единицу измерения.
        category_id=row[3],  # Записываем ID категории продукта.
    )  # Завершаем создание объекта Product.


def get_all() -> list[Product]:  # Объявляем функцию получения всех продуктов.
    with get_connection() as connection:  # Получаем подключение через контекстный менеджер.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запроса.
        cursor.execute(  # Выполняем запрос на получение продуктов.
            "SELECT product_id, name, unit, category_id "  # Выбираем поля продукта.
            "FROM products ORDER BY product_id"  # Указываем таблицу и сортировку.
        )  # Завершаем выполнение запроса.
        rows = cursor.fetchall()  # Получаем все найденные строки.
        return [_map(row) for row in rows]  # Преобразуем строки в список моделей Product.


def get_by_id(product_id: int) -> Product | None:  # Объявляем функцию поиска продукта по ID.
    with get_connection() as connection:  # Получаем подключение через контекстный менеджер.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запроса.
        cursor.execute(  # Выполняем запрос на поиск одного продукта.
            "SELECT product_id, name, unit, category_id "  # Выбираем поля продукта.
            "FROM products WHERE product_id = ?",  # Ищем продукт с указанным ID.
            (product_id,),  # Передаём ID отдельно от SQL-команды.
        )  # Завершаем выполнение запроса.
        row = cursor.fetchone()  # Получаем одну строку или None.
        return _map(row) if row else None  # Возвращаем модель продукта либо None.


def create(name: str, unit: str, category_id: int) -> int:  # Объявляем функцию добавления продукта.
    with get_connection() as connection:  # Получаем подключение через контекстный менеджер.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запроса.
        cursor.execute(  # Выполняем запрос на добавление продукта.
            "INSERT INTO products (name, unit, category_id) "  # Указываем таблицу и поля.
            "VALUES (?, ?, ?)",  # Используем параметры вместо вставки значений в SQL-текст.
            (name, unit, category_id),  # Передаём значения для нового продукта.
        )  # Завершаем выполнение запроса.
        connection.commit()  # Сохраняем добавленную запись в базе данных.
        return cursor.lastrowid  # Возвращаем ID добавленного продукта.


def update(  # Объявляем функцию изменения продукта.
    product_id: int,  # Указываем ID изменяемого продукта.
    name: str,  # Указываем новое название продукта.
    unit: str,  # Указываем новую единицу измерения.
    category_id: int,  # Указываем новую категорию продукта.
) -> bool:  # Функция возвращает True, если запись была изменена.
    with get_connection() as connection:  # Получаем подключение через контекстный менеджер.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запроса.
        cursor.execute(  # Выполняем запрос на изменение продукта.
            "UPDATE products SET name = ?, unit = ?, category_id = ? "  # Обновляем поля продукта.
            "WHERE product_id = ?",  # Ограничиваем изменение продуктом с указанным ID.
            (name, unit, category_id, product_id),  # Передаём новые значения и ID.
        )  # Завершаем выполнение запроса.
        connection.commit()  # Сохраняем изменения в базе данных.
        return cursor.rowcount > 0  # Возвращаем True, если была изменена хотя бы одна строка.


def delete(product_id: int) -> bool:  # Объявляем функцию удаления продукта по ID.
    with get_connection() as connection:  # Получаем подключение через контекстный менеджер.
        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запроса.
        cursor.execute(  # Выполняем запрос на удаление продукта.
            "DELETE FROM products WHERE product_id = ?",  # Удаляем продукт с указанным ID.
            (product_id,),  # Передаём ID отдельно от SQL-команды.
        )  # Завершаем выполнение запроса.
        connection.commit()  # Сохраняем удаление в базе данных.
        return cursor.rowcount > 0  # Возвращаем True, если была удалена хотя бы одна строка.