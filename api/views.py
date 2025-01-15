from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from .serializers import OrderSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

class OrderListCreateAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '').strip()
        orders = Order.objects.all()

        if query:
            orders = orders.filter(
                Q(table_number__icontains=query) |
                Q(status__icontains=query)
            )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
