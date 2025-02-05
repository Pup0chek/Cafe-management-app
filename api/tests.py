from unittest import mock
from rest_framework.test import APITestCase
from orders.models import Item, Order, OrderItem
from rest_framework.response import Response
from typing import Dict, Any, List


class OrderAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Создание тестовых данных
        cls.item1 = Item.objects.create(name="Item 1", price=100)
        cls.item2 = Item.objects.create(name="Item 2", price=200)
        cls.order1 = Order.objects.create(table_number=1, status="pending")
        cls.order2 = Order.objects.create(table_number=2, status="paid")
        OrderItem.objects.create(order=cls.order1, item=cls.item1, quantity=2)
        OrderItem.objects.create(order=cls.order2, item=cls.item2, quantity=3)

    @mock.patch('psycopg2.connect')
    def test_get_order_list(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        response: Response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    @mock.patch('psycopg2.connect')
    def test_filter_order_by_status(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        response: Response = self.client.get('/api/orders/', {'status': 'paid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['table_number'], 2)

    @mock.patch('psycopg2.connect')
    def test_create_order(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        payload: Dict[str, Any] = {
            'table_number': 3,
            'items': [
                {'item': self.item1.id, 'quantity': 1},
                {'item': self.item2.id, 'quantity': 2}
            ]
        }
        response: Response = self.client.post('/api/orders/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 3)

    @mock.patch('psycopg2.connect')
    def test_get_order_detail(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        response: Response = self.client.get(f'/api/orders/{self.order1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['table_number'], 1)

    @mock.patch('psycopg2.connect')
    def test_patch_order(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        payload: Dict[str, Any] = {'status': 'ready'}
        response: Response = self.client.patch(f'/api/orders/{self.order1.id}/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'ready')

    @mock.patch('psycopg2.connect')
    def test_delete_order(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        response: Response = self.client.delete(f'/api/orders/{self.order1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 1)


class ItemAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Убедимся, что база данных очищена
        Item.objects.all().delete()

        # Создание тестовых данных
        cls.item1 = Item.objects.create(name="Item 1", price=100)
        cls.item2 = Item.objects.create(name="Item 2", price=200)

    @mock.patch('psycopg2.connect')
    def test_get_item_list(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        # Проверяем, что создаем ровно два объекта
        self.assertEqual(Item.objects.count(), 2)

        response: Response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)

        # Убедимся, что API возвращает только созданные объекты
        returned_items: List[Dict[str, Any]] = response.data
        self.assertEqual(len(returned_items), 2)
        self.assertEqual(returned_items[0]['name'], self.item1.name)
        self.assertEqual(returned_items[1]['name'], self.item2.name)

    @mock.patch('psycopg2.connect')
    def test_get_item_detail(self, mock_connect) -> None:
        # Мокаем соединение с БД
        mock_connect.return_value = None

        response: Response = self.client.get(f'/api/items/{self.item1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Item 1')
