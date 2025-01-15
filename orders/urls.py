from django.urls import path
from orders.views import *



urlpatterns = [
    path('', order_list, name='order_list'),
    path('/orders/add/', add_order, name='add_order'),
    path('/orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('/orders/revenue/', revenue, name='revenue'),
    path('/orders/change_status/<int:order_id>/', change_order_status, name='change_order_status'),
]

