from database import get_connection  # Импортируем подключение к базе данных.
from models import User  # Импортируем модель пользователя.


def _map(row) -> User:  # Преобразуем строку базы данных в объект User.
    return User(  # Создаём объект пользователя.
        user_id=row["user_id"],  # Получаем ID пользователя.
        login=row["login"],  # Получаем логин пользователя.
        role=row["role"],  # Получаем роль пользователя.
    )  # Завершаем создание объекта User.


def get_all() -> list[User]:  # Получаем список всех пользователей.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        rows = connection.execute(  # Выполняем запрос к таблице пользователей.
            "SELECT user_id, login, role FROM users ORDER BY user_id"  # Выбираем данные без паролей.
        ).fetchall()  # Получаем все строки результата.
    return [_map(row) for row in rows]  # Преобразуем строки в объекты User.


def get_by_id(user_id: int) -> User | None:  # Ищем пользователя по ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        row = connection.execute(  # Выполняем запрос для поиска пользователя.
            "SELECT user_id, login, role FROM users WHERE user_id = ?",  # Ищем по ID.
            (user_id,),  # Передаём ID отдельным параметром.
        ).fetchone()  # Получаем одну строку или None.
    return _map(row) if row else None  # Возвращаем пользователя или None.


def get_by_login(login: str) -> User | None:  # Ищем пользователя по логину.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        row = connection.execute(  # Выполняем запрос для поиска пользователя.
            "SELECT user_id, login, role FROM users WHERE login = ?",  # Ищем по логину.
            (login,),  # Передаём логин отдельным параметром.
        ).fetchone()  # Получаем одну строку или None.
    return _map(row) if row else None  # Возвращаем пользователя или None.


def get_credentials(login: str) -> tuple[str, str] | None:  # Получаем соль и хеш пароля для проверки входа.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        row = connection.execute(  # Выполняем запрос к данным для авторизации.
            "SELECT password_salt, password_hash FROM users WHERE login = ?",  # Выбираем только данные пароля.
            (login,),  # Передаём логин отдельным параметром.
        ).fetchone()  # Получаем одну строку или None.
    return (row["password_salt"], row["password_hash"]) if row else None  # Возвращаем соль и хеш или None.


def create(login: str, salt: str, password_hash: str, role: str) -> int:  # Создаём пользователя.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на добавление пользователя.
            "INSERT INTO users (login, password_salt, password_hash, role) VALUES (?, ?, ?, ?)",  # Добавляем данные параметрами.
            (login, salt, password_hash, role),  # Передаём логин, соль, хеш и роль.
        )  # Завершаем выполнение запроса.
        user_id = cursor.lastrowid  # Получаем ID созданного пользователя.
    return user_id  # Возвращаем ID пользователя.


def update_role(user_id: int, role: str) -> bool:  # Изменяем роль пользователя.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на изменение роли.
            "UPDATE users SET role = ? WHERE user_id = ?",  # Меняем роль пользователя с указанным ID.
            (role, user_id),  # Передаём новую роль и ID.
        )  # Завершаем выполнение запроса.
        updated = cursor.rowcount > 0  # Проверяем, была ли изменена запись.
    return updated  # Возвращаем результат операции.


def delete(user_id: int) -> bool:  # Удаляем пользователя по ID.
    with get_connection() as connection:  # Открываем подключение к базе данных.
        cursor = connection.execute(  # Выполняем запрос на удаление пользователя.
            "DELETE FROM users WHERE user_id = ?",  # Удаляем пользователя с указанным ID.
            (user_id,),  # Передаём ID отдельным параметром.
        )  # Завершаем выполнение запроса.
        deleted = cursor.rowcount > 0  # Проверяем, была ли удалена запись.
    return deleted  # Возвращаем результат операции.