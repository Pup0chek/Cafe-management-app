from django.test import TestCase

# Create your tests here.
from orders.models import Item, Order, OrderItem


class OrderModelTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Item 1", price=100)
        self.order = Order.objects.create(table_number=1, status="pending")
        self.order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=2)

    def test_calculate_total_price(self):
        self.order.calculate_total_price()
        self.assertEqual(self.order.total_price, 200)
