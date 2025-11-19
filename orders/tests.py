from rest_framework.test import APITestCase
from rest_framework import status
from orders.models import Order, OrderItem, Item
from unittest.mock import patch, Mock
from django.test import TestCase, Client
from unittest.mock import patch
from orders.models import Item, Order, OrderItem
import json
from typing import Dict, Any
import os

API_BASE_URL =  os.getenv("API_BASE_URL", "http://localhost:8000/api/")


class OrderModelTests(TestCase):
    def setUp(self) -> None:
        self.item = Item.objects.create(name="Item 1", price=100)
        self.order = Order.objects.create(table_number=1, status="pending")
        self.order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=2)

    def test_calculate_total_price(self) -> None:
        self.order.calculate_total_price()
        self.assertEqual(self.order.total_price, 200)


class OrdersViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.api_base_url =  os.getenv("API_BASE_URL", "http://localhost:8000/api/")

        # Создаем тестовые данные
        self.item1 = Item.objects.create(name="Test Item 1", price=100)
        self.item2 = Item.objects.create(name="Test Item 2", price=200)

        self.order1 = Order.objects.create(table_number=1, status="pending")
        self.order2 = Order.objects.create(table_number=2, status="paid")

        OrderItem.objects.create(order=self.order1, item=self.item1, quantity=2)
        OrderItem.objects.create(order=self.order2, item=self.item2, quantity=1)

    @patch('requests.get')
    def test_order_list_view(self, mock_get) -> None:
        # Мокаем ответы от API
        mock_get.side_effect = [
            Mock(json=lambda: [("pending", "Ожидание"), ("paid", "Оплачено")], status_code=200),  # Статусы
            Mock(json=lambda: [{"id": 1, "table_number": 1, "status": "pending", "total_price": 100}], status_code=200)  # Заказы
        ]

        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ожидание")
        self.assertContains(response, "Оплачено")
        self.assertContains(response, "Заказы")

    @patch('requests.post')
    @patch('requests.get')
    def test_add_order_view(self, mock_get, mock_post) -> None:
        """Тест для добавления заказа"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": self.item1.id, "name": self.item1.name},
            {"id": self.item2.id, "name": self.item2.name},
        ]

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "id": 3, "table_number": 3, "status": "pending", "total_price": 300
        }

        response = self.client.post(
            '/orders/add/',
            {
                'table_number': 3,
                'form-0-item': self.item1.id,
                'form-0-quantity': 3,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
            }
        )
        self.assertEqual(response.status_code, 302)

    @patch('requests.get')
    def test_revenue_view(self, mock_get) -> None:
        """Тест для получения общей выручки"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": self.order2.id, "status": "paid", "total_price": 200}
        ]

        response = self.client.get('/orders/revenue/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "200")
