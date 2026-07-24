## Задача 1. SQLAlchemy — Моделирование системы управления задачами

### Описание
Необходимо смоделировать систему управления задачами (аналог Trello или Jira) с помощью **SQLAlchemy**.
Основное внимание уделяется корректному описанию таблиц, типов данных, связей и ограничений.
После описания моделей необходимо создать и применить миграцию с помощью **Alembic**.

### Требования к реализации

#### Модель `User`
- `id`: UUID — Primary Key
- `full_name`: String(100) — Not Null
- `email`: String(120) — Not Null, Unique
- `created_at`: DateTime — Not Null, по умолчанию `datetime.utcnow`

#### Модель `Task`
- `id`: UUID — Primary Key
- `title`: String(255) — Not Null
- `description`: Text
- `status`: Enum — Not Null (`'todo'`, `'in_progress'`, `'done'`)
- `created_at`: DateTime — Not Null, default=`datetime.utcnow`, Indexed
- `author_id`: UUID — ForeignKey → `user.id`, Not Null
- `assignee_id`: UUID — ForeignKey → `user.id`, Nullable
- `column_id`: UUID — ForeignKey → `column.id`, Nullable
- `sprint_id`: UUID — ForeignKey → `sprint.id`, Nullable
- `board_id`: UUID — ForeignKey → `board.id`, Nullable
- `group_id`: UUID — ForeignKey → `group.id`, Nullable

#### Многие ко многим
- `task_watchers` — пользователи-наблюдатели
- `task_executors` — пользователи-исполнители

#### Модель `Board`
- `id`: UUID — Primary Key
- `name`: String(100) — Not Null, Unique

#### Модель `Column`
- `id`: UUID — Primary Key
- `name`: String(100) — Not Null
- `board_id`: UUID — ForeignKey → `board.id`

#### Модель `Sprint`
- `id`: UUID — Primary Key
- `name`: String(100) — Not Null
- `start_date`: Date
- `end_date`: Date

#### Модель `Group`
- `id`: UUID — Primary Key
- `name`: String(100) — Not Null, Unique

### Подсказки
- Используйте Enum-тип для поля `status`:
  `Enum('todo', 'in_progress', 'done', name='task_status')`
- Для поля `created_at` добавьте `index=True`
- Используйте ограничения: `nullable=False`, `unique=True`, `ForeignKey`, `Check(...)` — где уместно

### Критерии оценки
- Все связи между моделями описаны корректно
- Использован хотя бы один Enum
- Добавлены ограничения и индекс
- Создана и применена миграция Alembic


# Создание и применение миграций с помощью Alembic

Этот раздел поясняет, как создавать и применять миграции в проекте с использованием Alembic. Убедитесь, что вы следуете всем инструкциям, чтобы эффективно управлять схемой базы данных.

## Шаг 1: Установите Alembic

Если Alembic еще не установлен в вашем проекте, выполните следующую команду:

```bash
pip install alembic

## Шаг 2: Инициализация Alembic

alembic init alembic

## Шаг 3: Настройка конфигурации

Откройте файл alembic.ini и найдите следующую строку:
sqlalchemy.url = driver://user:pass@localhost/dbname

Замените её на строку подключения к вашей базе данных. Пример:
sqlalchemy.url = postgresql://username:password@localhost:5432/database_name

## Шаг 4: Создание миграции
alembic revision --autogenerate -m "Описание миграции"

## Шаг 5: Применение миграции
alembic upgrade head


## Задача 2. Redis — Простое кэширование данных пользователя

### Описание
Необходимо реализовать простое кэш-хранилище в **Redis**, которое сохраняет и извлекает данные о пользователях.  
Ключ формируется по шаблону `user:{user_id}`, а значение хранит строку с ФИО пользователя.

### Требования к реализации
Создайте класс `RedisRepository` с методами:
- `set_user(user_id: int, full_name: str)` — сохранить данные  
- `get_user(user_id: int)` — получить данные  
- `delete_user(user_id: int)` — удалить данные  

Данные хранятся в виде строки (`str`) по ключу `user:{user_id}`.  
Подключение к Redis должно быть передано через конструктор.

### Подсказки
- Используйте библиотеку `redis-py` (или `redis.asyncio` для асинхронной версии)  
- Не забудьте сериализовать и десериализовать строковые значения при необходимости  

### Критерии оценки
- Методы корректно работают с Redis  
- Ключи формируются строго по шаблону `user:{id}`  
- Использована строгая типизация  
- Реализована проверка корректности (тесты или ручное тестирование)  

