from rest_framework import serializers
from orders.models import Order, OrderItem, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'total_price', 'items']
