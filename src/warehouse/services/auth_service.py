import hashlib  # Подключаем безопасное хеширование паролей.
import hmac  # Подключаем безопасное сравнение хешей.
import secrets  # Подключаем генератор случайной соли для паролей.
from repositories import user_repository  # Импортируем репозиторий пользователей.


ROLE_NAMES = {  # Храним названия ролей для меню и отображения.
    "admin": "Администратор",  # Роль администратора.
    "warehouse_keeper": "Кладовщик",  # Роль кладовщика.
    "procurement_manager": "Менеджер по закупкам",  # Роль менеджера по закупкам.
    "accountant": "Бухгалтер",  # Роль бухгалтера.
}  # Завершаем список ролей.


def get_all_users():  # Получаем список пользователей.
    return user_repository.get_all()  # Возвращаем пользователей из репозитория.


def register_user(login: str, password: str, role: str) -> int:  # Проверяем данные и создаём пользователя.
    login = login.strip()  # Удаляем лишние пробелы у логина.
    if not login:  # Проверяем, что логин не пустой.
        raise ValueError("Логин не может быть пустым")  # Сообщаем об ошибке логина.
    if len(password) < 6:  # Проверяем минимальную длину пароля.
        raise ValueError("Пароль должен содержать не менее 6 символов")  # Сообщаем об ошибке пароля.
    if role not in ROLE_NAMES:  # Проверяем, что указана существующая роль.
        raise ValueError("Выбрана неизвестная роль")  # Сообщаем об ошибке роли.
    if user_repository.get_by_login(login):  # Проверяем, занят ли логин.
        raise ValueError("Пользователь с таким логином уже существует")  # Сообщаем о занятом логине.
    salt = secrets.token_bytes(16).hex()  # Создаём уникальную случайную соль.
    password_hash = hashlib.pbkdf2_hmac(  # Вычисляем стойкий хеш пароля.
        "sha256",  # Используем алгоритм SHA-256.
        password.encode("utf-8"),  # Преобразуем пароль в байты.
        bytes.fromhex(salt),  # Используем соль для этого пользователя.
        200_000,  # Повторяем вычисление, чтобы усложнить подбор пароля.
    ).hex()  # Преобразуем итоговый хеш в строку.
    return user_repository.create(login, salt, password_hash, role)  # Сохраняем пользователя в базе данных.


def authenticate(login: str, password: str):  # Проверяем логин и пароль пользователя.
    login = login.strip()  # Удаляем лишние пробелы у логина.
    credentials = user_repository.get_credentials(login)  # Получаем соль и сохранённый хеш.
    if not credentials:  # Проверяем, найден ли пользователь.
        return None  # Возвращаем None, если логин не найден.
    salt, saved_hash = credentials  # Разделяем соль и сохранённый хеш.
    entered_hash = hashlib.pbkdf2_hmac(  # Вычисляем хеш введённого пароля.
        "sha256",  # Используем алгоритм SHA-256.
        password.encode("utf-8"),  # Преобразуем введённый пароль в байты.
        bytes.fromhex(salt),  # Используем соль пользователя.
        200_000,  # Используем те же параметры хеширования.
    ).hex()  # Преобразуем полученный хеш в строку.
    if not hmac.compare_digest(entered_hash, saved_hash):  # Безопасно сравниваем хеши.
        return None  # Возвращаем None, если пароль неверный.
    return user_repository.get_by_login(login)  # Возвращаем пользователя после успешной проверки.