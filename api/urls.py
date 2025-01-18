from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    ItemListAPIView,
    ItemDetailAPIView,
    StatusListAPIView,
    get_revenue
)

urlpatterns = [
    # Маршруты для заказов
    path('orders/', OrderListCreateAPIView.as_view(), name='api_order_list_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='api_order_detail'),

    # Маршруты для товаров
    path('items/', ItemListAPIView.as_view(), name='api_item_list'),
    path('items/<int:pk>/', ItemDetailAPIView.as_view(), name='api_item_detail'),

    path('revenue/', get_revenue, name='api_get_revenue'),
    path('statuses/', StatusListAPIView.as_view(), name='api_status_list'),
]
