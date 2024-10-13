# Calorie Counter Application

## Описание
Это простое веб-приложение для добавления блюд и подсчета калорий. Оно использует Flask для создания веб-интерфейса и PostgreSQL для хранения данных.

## Запуск приложения

### Требования:
- Docker
- Docker Compose

### Шаги:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/calorie_counter.git
   cd calorie_counter
   ```

2. Запустите приложение:
   ```bash
   docker-compose up
   ```

3. Приложение будет доступно по адресу `http://localhost:5000`.

## Структура проекта
- `app.py` — основной файл приложения Flask.
- `db.py` — функции для взаимодействия с базой данных.
- `Dockerfile` — конфигурация для сборки Docker-образа.
- `docker-compose.yml` — файл для управления контейнерами Docker.
- `requirements.txt` — зависимости Python.
- `templates/` — HTML-шаблоны.
