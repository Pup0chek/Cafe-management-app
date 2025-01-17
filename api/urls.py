from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView


urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='api_order_list_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='api_order_detail'),
]
