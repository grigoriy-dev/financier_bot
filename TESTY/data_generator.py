"""
Модуль для генерации тестовых данных транзакций.

Этот модуль предоставляет функцию для генерации случайных транзакций, которые могут быть использованы
для тестирования и заполнения базы данных.

Основные функции:
- `random_date`: Генерация случайной даты и времени в заданном диапазоне.
- `generate_data`: Генерация списка транзакций с случайными данными.

Структура данных:
- Пользователи: Список пользователей с их telegram_id и username.
- Категории: Список категорий (Доходы и Расходы).
- Подкатегории: Список подкатегорий, связанных с категориями.
- Транзакции: Список транзакций, содержащих дату, пользователя, категорию, подкатегорию, сумму и комментарий.

Пример использования:
- Генерация 50 случайных транзакций для тестирования.

Примечание:
- Данные генерируются в диапазоне дат с 1 января 2025 года по 25 февраля 2025 года.
- Вероятность генерации дохода составляет 30%, а расхода — 70%.
- Комментарий к транзакции добавляется с вероятностью 50%.
"""

import random
from datetime import datetime, timedelta

# Список пользователей
users = [
    {'telegram_id': 84779623, 'username': 'BobaFett', 'id': 1},
    {'telegram_id': 12345678, 'username': 'LandoCalrissian', 'id': 2},
    {'telegram_id': 87654321, 'username': 'ObiWanKenobi', 'id': 3},
    {'telegram_id': 98765432, 'username': 'HanSolo', 'id': 4},
    {'telegram_id': 56781234, 'username': 'PrincessLeia', 'id': 5},
    {'telegram_id': 43218765, 'username': 'MaceWindu', 'id': 6},
    {'telegram_id': 67358500, 'username': 'SkyWalker', 'id': 7}
]

# Список категорий
categories = [
    {"name": "Доход", 'id': 1},
    {"name": "Расход", 'id': 2}
]

# Список подкатегорий
subcategories = [
    {'category_id': 1, 'name': 'Зарплата', 'id': 1},
    {'category_id': 1, 'name': 'Инвестиции', 'id': 2},
    {'category_id': 1, 'name': 'Фриланс', 'id': 3},
    {'category_id': 1, 'name': 'Подарки', 'id': 4},
    {'category_id': 1, 'name': 'Другое', 'id': 5},
    {'category_id': 2, 'name': 'Еда', 'id': 6},
    {'category_id': 2, 'name': 'Транспорт', 'id': 7},
    {'category_id': 2, 'name': 'Жилье', 'id': 8},
    {'category_id': 2, 'name': 'Одежда', 'id': 9},
    {'category_id': 2, 'name': 'Здоровье', 'id': 10},
    {'category_id': 2, 'name': 'Развлечения', 'id': 11},
    {'category_id': 2, 'name': 'Подарки', 'id': 12},
    {'category_id': 2, 'name': 'Связь', 'id': 13},
    {'category_id': 2, 'name': 'Путешествия', 'id': 14},
    {'category_id': 2, 'name': 'Долги', 'id': 15},
    {'category_id': 2, 'name': 'Другое', 'id': 16}
]

# Функция для генерации случайной даты и времени в заданном диапазоне
def random_date(start, end):
    """
    Генерирует случайную дату и время в заданном диапазоне.
    
    Args:
        start (datetime): Начальная дата.
        end (datetime): Конечная дата.
    
    Returns:
        datetime: Случайная дата и время.
    """
    random_days = random.randint(0, (end - start).days)  # Случайное количество дней
    random_seconds = random.randint(0, 86400)  # Случайное количество секунд в пределах дня (86400 секунд = 24 часа)
    
    return start + timedelta(days=random_days, seconds=random_seconds)

# Начальная и конечная даты
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 2, 25)

# Генерация 50 записей
def generate_data():
    transactions = []
    for _ in range(10000):
        date = random_date(start_date, end_date)
        user = random.choice(users)
        category_id = random.choices([1, 2], weights=[0.3, 0.7])[0]  # 30% доходы, 70% расходы
        subcategory = random.choice([sc for sc in subcategories if sc['category_id'] == category_id])
        amount = random.randint(100, 10000)  # Сумма от 100 до 10000
        comment = random.choice([None, "Комментарий к транзакции"])  # 50% вероятность комментария
        
        transaction = {
            'date': date,
            'user_telegram_id': user['telegram_id'],
            'category_id': category_id,
            'subcategory_id': subcategory['id'],
            'amount': amount,
            'comment': comment
        }
        
        transactions.append(transaction)
    return transactions
