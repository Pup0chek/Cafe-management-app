# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /code

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /code/

# Команда запуска сервера
CMD ["gunicorn", "cafe_order_management.wsgi:application", "--bind", "0.0.0.0:8000"]
