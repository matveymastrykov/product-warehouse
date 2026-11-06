from models import Stock  # Импортируем модель остатка для аннотации типа.
from repositories import stock_repository  # Импортируем репозиторий остатков.


def get_stock() -> list[Stock]:  # Указываем, что функция возвращает список объектов Stock.
    return stock_repository.get_stock()  # Получаем рассчитанные остатки из репозитория.