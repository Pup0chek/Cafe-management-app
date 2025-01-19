from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Item
import random
from typing import Dict

@receiver(post_migrate)
def create_default_items(sender: object, **kwargs: Dict) -> None:
    # Убедимся, что сигнал срабатывает только для приложения `orders`
    if sender.name != 'orders':
        return

    # Если в таблице уже есть записи, ничего не делаем
    if Item.objects.exists():
        return

    # Список названий для блюд
    dishes: list[str] = [
        "Салат Цезарь", "Борщ", "Пельмени", "Оливье", "Шашлык", "Котлета по-киевски",
        "Суп-харчо", "Блины с икрой", "Жаркое", "Картофельное пюре", "Паста Карбонара",
        "Пицца Маргарита", "Ризотто", "Тирамису", "Мороженое", "Чизкейк", "Баклажаны по-грузински",
        "Лагман", "Манты", "Плов", "Куриный шашлык", "Греческий салат", "Сырники", "Уха",
        "Жульен", "Селёдка под шубой", "Тыквенный суп", "Гуляш", "Куриные наггетсы",
        "Французские тосты", "Круассан", "Салат с тунцом", "Бургер", "Хот-дог", "Карбонад",
        "Паштет", "Куриный бульон", "Сэндвич с ветчиной", "Фрикадельки", "Суп Минестроне",
        "Чахохбили", "Шаурма", "Куриный стейк", "Свинина на гриле", "Лосось на пару", 
        "Омлет", "Салат Нисуаз", "Гаспачо", "Брускетта", "Рататуй", "Пирог с яблоками"
    ]

    # Создаём 100 случайных блюд
    items_to_create: list[Item] = []
    for _ in range(100):
        dish_name: str = random.choice(dishes)  # Случайное название блюда
        price: int = random.randint(100, 1500)  # Случайная цена от 100 до 1500 рублей
        items_to_create.append(Item(name=dish_name, price=price))
    
    # Сохраняем все записи за один запрос
    Item.objects.bulk_create(items_to_create)
