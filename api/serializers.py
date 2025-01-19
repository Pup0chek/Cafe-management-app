from rest_framework import serializers
from orders.models import Order, OrderItem, Item
from django.db.models import Sum, F
from typing import Any, Dict, List


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения товаров.
    """
    class Meta:
        model = Item
        fields = ['id', 'name', 'price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания элементов заказа.
    """
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения элементов заказа.
    """
    item_name = serializers.CharField(source='item.name')  # Отображаем имя товара
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2)  # Отображаем цену товара

    class Meta:
        model = OrderItem
        fields = ('item_name', 'item_price', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания заказа.
    """
    items = OrderItemCreateSerializer(many=True)  # Вложенный сериализатор для элементов заказа

    class Meta:
        model = Order
        fields = ('table_number', 'status', 'items')

    def create(self, validated_data: Dict[str, Any]) -> Order:
        """
        Создание заказа и связанных элементов.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.calculate_total_price()
        order.save()

        return order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения заказа.
    """
    items = OrderItemSerializer(many=True)  # Вложенный сериализатор для отображения элементов заказа

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'status', 'items', 'total_price')

    def get_total_price(self, obj: Order) -> float:
        """
        Динамически рассчитывает общую стоимость заказа.
        """
        total = obj.items.aggregate(
            total=Sum(F('quantity') * F('item__price'))
        )['total'] or 0
        return total
