from dataclasses import dataclass  # Подключаем декоратор для создания классов данных


@dataclass  # Автоматически создаёт конструктор класса и другие полезные методы
class Category:  # Модель категории, соответствует таблице categories
    category_id: int  # ID категории, целое число
    name: str  # Название категории, строка


@dataclass  # Объявляем класс данных
class Supplier:  # Модель поставщика, соответствует таблице suppliers
    supplier_id: int  # ID поставщика
    name: str  # Название поставщика
    phone: str | None = None  # Телефон или None, если телефон не указан


@dataclass  # Объявляем класс данных
class Product:  # Модель продукта, соответствует таблице products
    product_id: int  # ID продукта
    name: str  # Название продукта
    unit: str  # Единица измерения, например «кг» или «л»
    category_id: int  # ID категории, к которой относится продукт


@dataclass  # Объявляем класс данных
class Delivery:  # Модель поставки, соответствует таблице deliveries
    delivery_id: int  # ID поставки
    supplier_id: int  # ID поставщика, который выполнил поставку
    delivery_date: str  # Дата поставки в виде строки


@dataclass  # Объявляем класс данных
class DeliveryItem:  # Модель позиции поставки, соответствует таблице delivery_items
    item_id: int  # ID позиции поставки
    delivery_id: int  # ID поставки, к которой относится позиция
    product_id: int  # ID поставленного продукта
    quantity: int  # Количество продукта
    unit_price: float  # Цена одной единицы продукта
    expiration_date: str  # Срок годности в виде строки


@dataclass  # Объявляем класс данных
class Writeoff:  # Модель списания, соответствует таблице writeoffs
    writeoff_id: int  # ID списания
    writeoff_date: str  # Дата списания в виде строки
    reason: str  # Причина списания


@dataclass  # Объявляем класс данных
class WriteoffItem:  # Модель позиции списания, соответствует таблице writeoff_items
    writeoff_item_id: int  # ID записи о списании
    writeoff_id: int  # ID списания
    item_id: int  # ID позиции поставки, которую списывают
    quantity: int  # Количество списанного продукта
@dataclass  # Объявляем класс моделью данных.
class Stock:  # Описываем остаток одного продукта.
    product_name: str  # Храним название продукта.
    category_name: str  # Храним название категории.
    quantity: int  # Храним количество продукта на складе.
@dataclass  # Объявляем модель пользователя.
class User:  # Храним основные данные пользователя без пароля.
    user_id: int  # ID пользователя в базе данных.
    login: str  # Логин пользователя.
    role: str  # Роль пользователя в системе.