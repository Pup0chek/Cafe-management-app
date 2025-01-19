from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from orders.models import Order, OrderItem, Item
from .serializers import OrderSerializer, OrderCreateSerializer, ItemSerializer
from django.db import models
from rest_framework.request import Request
from typing import Any


class OrderListCreateAPIView(APIView):
    """
    API для работы со списком заказов:
    - GET: Список заказов с фильтрацией.
    - POST: Создание нового заказа.
    """
    def get(self, request: Request) -> Response:
        table_number = request.query_params.get('table_number')
        status = request.query_params.get('status')

        orders = Order.objects.prefetch_related('items__item')

        if table_number:
            orders = orders.filter(table_number=table_number)
        if status:
            orders = orders.filter(status=status)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """
    API для работы с конкретным заказом:
    - GET: Получение деталей заказа.
    - PATCH: Частичное обновление заказа.
    - DELETE: Удаление заказа.
    """
    def get(self, request: Request, pk: int) -> Response:
        order = get_object_or_404(Order.objects.prefetch_related('items__item'), pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            order.calculate_total_price()
            order.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemListAPIView(APIView):
    """
    API для получения списка товаров.
    """
    def get(self, request: Request) -> Response:
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class ItemDetailAPIView(APIView):
    """
    API для работы с конкретным товаром.
    """
    def get(self, request: Request, pk: int) -> Response:
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


@api_view(['GET'])
def get_revenue(request: Request) -> Response:
    """
    API для получения общей выручки.
    """
    try:
        total_revenue = Order.objects.filter(status='paid').aggregate(
            total=models.Sum('total_price')
        )['total'] or 0
        return Response({'total_revenue': total_revenue})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatusListAPIView(APIView):
    """API для получения списка статусов."""
    def get(self, request: Request) -> Response:
        return Response(Order.STATUS_CHOICES)
