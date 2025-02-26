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

# Функция для генерации случайной даты в заданном диапазоне
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Начальная и конечная даты
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 2, 25)

# Генерация 50 записей
def generate_data():
    transactions = []
    for _ in range(50):
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
