# ToDo Telegram Bot
Проект представляет собой телеграм-бота для управления задачами (ToDo List), интегрированного с бэкендом на Django через REST API. Реализованы CRUD-операции для задач, уведомления о дедлайнах через Celery и диалоговое взаимодействие через Aiogram-Dialog (стоит отметить, что я не стал реализовывать функционал просмотра, выбора и редактирования категорий напрямую, пользователь может ввести название любой (и старой и новой)). Проект развертывается с использованием Docker.


# Инструкция по запуску

## Требования

- Docker и Docker Compose
- Переменные окружения (см. .env.example)

## Шаги для запуска

### Клонируйте репозиторий:
git clone <ссылка_на_репозиторий>

cd todo_tg_bot_project


### Создайте файл
.env:Скопируйте .env.example в .env и заполните переменные:
cp .env.example .env

Пример .env:

DJANGO_SECRET_KEY=ваш_секретный_ключ

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1,backend

POSTGRES_DB=todo_db

POSTGRES_USER=todo_user

POSTGRES_PASSWORD=ваш_пароль

POSTGRES_HOST=db

POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

BOT_TOKEN=ваш_токен_бота

API_BASE_URL=http://backend:8000/api/


### Запустите проект:
docker-compose up --build


### Проверьте доступность:

Django Admin: http://localhost:8000/admin/ (создайте суперпользователя командой docker-compose exec backend python manage.py createsuperuser).

Telegram-бот: Найдите бота в Telegram по токену и используйте команды /start, /add_task, /show_tasks.




## Архитектура решения

### Django (бэкенд):

Модели: UserProfile (связь с Telegram ID), Task (задачи), Category (категории).

API: REST API для задач (/api/tasks/) и привязки Telegram ID (/api/link_telegram_id/).

Celery: Уведомления о дедлайнах через задачу check_due_tasks, запускаемую каждую минуту.

Админ-панель: Управление задачами, категориями и профилями.

База данных: PostgreSQL, Redis для Celery.

Часовой пояс: America/Adak.


### Aiogram (телеграм-бот):

Функции: Просмотр задач с датой создания, добавление задач через диалог, удаление, завершение и редактирование.

Диалоги: aiogram-dialog для пошагового ввода данных задачи (название, описание, дедлайн, категории).

Интеграция: Асинхронные запросы к Django API через aiohttp.

### Docker:

Сервисы: db (PostgreSQL), redis, backend (Django), celery, celery-beat, bot (Aiogram).

Синхронизация: Используется wait-for-it.sh для ожидания готовности сервисов.





#Трудности и их решения
### 1. Проблема с WSL для Docker Desktop

Трудность: Ошибка "WSL update failed" блокировала запуск Docker Desktop из-за устаревшего WSL, конфликтов VPN или отсутствия Windows Features.

Решение: Переустановка WSL (wsl --install, wsl --update), активация Windows Features, устранение конфликтов и проверка виртуализации в BIOS.

### 2. Кастомный первичный ключ

Трудность: Запрет на UUID, random и автоинкременты усложнял создание уникальных PK, рискуя целостностью данных.

Решение: Хэш SHA-256 от user_id и timestamp с проверкой уникальности через Django ORM.

### 3. Интеграция Celery и Telegram-уведомлений

Трудность: Отправка асинхронных уведомлений из синхронной Celery-задачи, риски блокировок и пропуска уведомлений.

Решение: Асинхронная функция через aiohttp, вызов через asyncio.run_until_complete с обработкой ошибок.

### 4. Интеграция Django API с Telegram-ботом

Трудность: Сложности с аутентификацией, передачей Telegram ID и обработкой ошибок при асинхронных запросах.

Решение: Реализация API-клиента с aiohttp, модель UserProfile для Telegram ID, аутентификация через токены и обработка ошибок.

### 5. Контейнеризация и управление зависимостями

Трудность: Сложности с управлением зависимостями и порядком запуска сервисов в docker-compose.

Решение: Настройка Dockerfile и docker-compose.yml с depends_on, healthcheck и переменными из .env.




