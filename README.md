# Финансовый бот для Telegram 💰  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)  [![Aiogram](https://img.shields.io/badge/Aiogram-3.18.0-green)](https://docs.aiogram.dev/)  [![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-lightgrey)](https://fastapi.tiangolo.com/)  

Бот для удобного учета личных финансов с возможностью добавления доходов/расходов, категоризации и аналитики.  

## 📌 Основные возможности  

- Добавление доходов и расходов по категориям  
- Генерация отчетов за выбранный период (с пагинацией и без) в формате xlsx
- Гибкая система категорий и подкатегорий  
- Хранение данных в SQLite/Redis  
- Веб-интерфейс через FastAPI для администрирования  
- Подробное логирование всех операций
- Адаптивные клавиатуры (автоматически подстраиваются под экран) 

## 🛠 Технологический стек  

Основные зависимости:  
- **Alembic** (1.15.1) - для миграций базы данных  
- **Aiosqlite** (0.21.0) - асинхронная работа с SQLite  
- **Loguru** (0.7.3) - удобное логирование  
- **Pydantic** (2.10.6) - валидация данных  
- **FastAPI** (0.115.11) - веб-интерфейс  
- **Aioredis** (2.0.1) - работа с Redis  
- **Pandas** (2.2.2) - анализ данных  
- **Aiogram** (3.18.0) - Telegram бот  
- **SQLAlchemy** (2.0.38) - ORM  

## 📋 Категории учета  

### Доходы:  
- 💼 **Зарплата**: Основной доход от работы  
- 📈 **Инвестиции**: Доход от акций, вкладов, криптовалюты  
- 🖥 **Фриланс**: Доход от проектов и подработок  
- 🎁 **Подарки**: Подарки, бонусы, премии  
- ✨ **Другое**: Прочие доходы  

### Расходы:  
- 🍏 **Еда**: Продукты питания и напитки  
- 🚕 **Транспорт**: Общественный транспорт, топливо  
- 🏠 **Жилье**: Аренда, коммунальные услуги  
- 👕 **Одежда**: Одежда, обувь, аксессуары  
- 🏥 **Здоровье**: Медицина, лекарства, спортзал  
- 🎭 **Развлечения**: Кино, рестораны, хобби  
- 🎁 **Подарки**: Подарки для близких  
- 📱 **Связь**: Интернет, мобильная связь  
- ✈ **Путешествия**: Транспорт, проживание  
- 💳 **Долги**: Погашение кредитов  
- ❓ **Другое**: Прочие расходы  


## 1. API (FastAPI)  
Основные эндпоинты:  
- Получение списка всех таблиц в базе данных.
- Получение всех записей для указанной модели с возможностью фильтрации и пагинации.
- Получение одной записи по идентификатору (например, telegram_id).
- Добавление одной или нескольких записей в указанную модель.
- Получение транзакций с объединением данных из связанных таблиц (пользователи, категории, подкатегории).

## 2. Работа с базой данных  
Универсальный класс MainGeneric предоставляет:  
- Базовые CRUD-операции  
- Поддержку асинхронных сессий  
- Возможности фильтрации и пагинации  
- Объединение данных из связанных таблиц  

## 3. Логирование  
Система логирования отслеживает:  
- Все действия пользователей с указанием ID пользователя и названием операции 
- Ошибки при формировании отчетов / обращении к БД
- Запросы к БД

## 4. Тестирование 
В каталоге TASTY есть инструменты для:
- Генерации тестовых данных (создание пользователей и транзакций)  
- Тестирования ручек API 


## ℹ Контактная информация  
- **Разработчик**: @thaigodtattoo  
- **Email**: georgeongit@gmail.com  
- **Версия**: v1.0  


## 🚀 Запуск проекта  
1. Установите зависимости:  
   `pip install -r requirements.txt`  
2. Создайте и настройте файл `.env`  
3. Запустите бота:  
   `python -m app.main`  

> Проект находится в активной разработке. Ваши предложения и сообщения об ошибках приветствуются!
