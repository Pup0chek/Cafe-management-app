# Cafe-management-app

Cafe-management-app — Этот проект представляет собой Django-приложение с микросервисной архитектурой. В нем реализованы два приложения: orders и API. Приложение orders выполняет основную логику работы с заказами и взаимодействует с базой данных через API. API реализует доступ к данным и позволяет выполнять операции с заказами, товарами и другими сущностями. Приложение API должно быть развернуто на другом сервере для обеспечения микросервисной архитектуры.

---

## Структура проекта
- orders — приложение, которое отвечает за работу с заказами, взаимодействует с API для работы с данными
- API — микросервис, предоставляющий API для работы с данными о заказах, товарах и статусах.


## Функциональность

1. ### Мониторинг заказов:
    Просмотр списка заказов с фильтрацией по статусу и номеру стола.
    Возможность обновлять статус заказа (например, "Ожидание", "Готово", "Оплачено").
    Создание новых заказов с выбором товаров и их количества.

2. ### API для взаимодействия:
    Все данные о заказах (включая статус и товары) обрабатываются через API.
    Микросервисная архитектура: API развернуто на отдельном сервере, а веб-приложение обращается к API для работы с данными.
    Возможность добавления, изменения и удаления заказов через API.

3. ### Хранение данных:
    Все данные о заказах и товарах хранятся в базе данных PostgreSQL.

4. ### Интерфейс:
    Удобный и интуитивно понятный интерфейс для пользователей.
    Простое создание и управление заказами, а также изменение их статусов.

5. ### Микросервисная архитектура:
    Разделение логики между двумя приложениями (orders и API).
    Приложение API предоставляет все необходимые данные через REST API, которые используются в интерфейсе заказов.

---

## Установка и запуск

1. Убедитесь, чтоб используете python3 или установите необходимую версию:
   ```bash
   apt install python3
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Pup0chek/Cafe-management-app.git
   cd Cafe-management-app
3. Для запуска проекта с помощью docker-compose выполните следующую команду:
   ```bash
   docker-compose up --build
4. Доступ к приложению
    ```bash
   http://localhost:8000/orders/

---

## Тестирование

Для запуска тестов выполните следующую команду:
    ```bash
   docker-compose exec web python manage.py test

---

## Примечания

- В этом проекте база данных PostgreSQL используется для хранения информации о заказах, товарах и связанных данных.
- Приложение API должно быть развернуто на отдельном сервере, так как оно является микросервисом для работы с данными.(Все запросы к базе данных ибрабатываются через API)

---

## Скриншоты программы

### Главная страница
![Главная страница](/orders/static/orders/main_page.png)

### Создание заказа
![Создание заказа](/orders/static/orders/add_order.png)
![Главная страница](/orders/static/orders/added_order.png)

### Изменение статуса
![Изменение статуса](/orders/static/orders/change_status.png)

### Общая выручка
![Общая выручка](/orders/static/orders/revenue.png)

### Тесты
![Тесты](/orders/static/orders/tests.png)
![Покрытие](/orders/static/orders/coverage.png)

---