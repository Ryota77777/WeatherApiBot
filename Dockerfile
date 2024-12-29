# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем необходимые зависимости для PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc

# Создаем и переходим в директорию для приложения
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Открываем порт
EXPOSE 8080

# Запускаем приложение
CMD ["python", "bot.py"]


