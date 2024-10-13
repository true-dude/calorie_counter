# Calorie Counter Application

## Описание

**Calorie Counter** — это веб-приложение для добавления блюд и подсчета калорий. Приложение использует **Flask** для создания веб-интерфейса, **PostgreSQL** для хранения данных и **Chart.js** для построения графиков потребления калорий за последние 10 минут.

## Требования

Перед началом работы убедитесь, что у вас установлены следующие программы:

- **Docker**: [Установка Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Установка Docker Compose](https://docs.docker.com/compose/install/)

## Установка и запуск приложения

1. **Клонирование репозитория**:

   Сначала клонируйте репозиторий с приложением на локальный компьютер:

   ```bash
   git clone https://github.com/your-repo/calorie_counter.git
   cd calorie_counter
2. **Запуск приложения в docker-compose**
    Выполните команду
    
    ```bash
    docker compose up --build -d
    ```
    Приложение будет доступно по адресу http://localhost:5000.

3. **Остановка приложения***    
    
    ```bash
    docker compose down
    ```

4. ***Видео обзор приложения***

   [Видео на Яндекс Диске](https://disk.yandex.ru/i/knW_3WwuljCcvA)