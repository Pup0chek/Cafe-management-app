from rest_framework.test import APITestCase
from orders.models import Item, Order, OrderItem


class OrderAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых данных
        cls.item1 = Item.objects.create(name="Item 1", price=100)
        cls.item2 = Item.objects.create(name="Item 2", price=200)
        cls.order1 = Order.objects.create(table_number=1, status="pending")
        cls.order2 = Order.objects.create(table_number=2, status="paid")
        OrderItem.objects.create(order=cls.order1, item=cls.item1, quantity=2)
        OrderItem.objects.create(order=cls.order2, item=cls.item2, quantity=3)

    def test_get_order_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_order_by_status(self):
        response = self.client.get('/api/orders/', {'status': 'paid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['table_number'], 2)

    def test_create_order(self):
        payload = {
            'table_number': 3,
            'items': [
                {'item': self.item1.id, 'quantity': 1},
                {'item': self.item2.id, 'quantity': 2}
            ]
        }
        response = self.client.post('/api/orders/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 3)

    def test_get_order_detail(self):
        response = self.client.get(f'/api/orders/{self.order1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['table_number'], 1)

    def test_patch_order(self):
        payload = {'status': 'ready'}
        response = self.client.patch(f'/api/orders/{self.order1.id}/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'ready')

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 1)


from rest_framework.test import APITestCase
from orders.models import Item

class ItemAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Убедимся, что база данных очищена
        Item.objects.all().delete()

        # Создание тестовых данных
        cls.item1 = Item.objects.create(name="Item 1", price=100)
        cls.item2 = Item.objects.create(name="Item 2", price=200)

    def test_get_item_list(self):
        # Проверяем, что создаем ровно два объекта
        self.assertEqual(Item.objects.count(), 2)

        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)

        # Убедимся, что API возвращает только созданные объекты
        returned_items = response.data
        self.assertEqual(len(returned_items), 2)
        self.assertEqual(returned_items[0]['name'], self.item1.name)
        self.assertEqual(returned_items[1]['name'], self.item2.name)

    def test_get_item_detail(self):
        response = self.client.get(f'/api/items/{self.item1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Item 1')
