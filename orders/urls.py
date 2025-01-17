from django.urls import path
from orders.views import *



urlpatterns = [
    path('', order_list, name='order_list'),
    path('add/', add_order, name='add_order'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
    path('revenue/', revenue, name='revenue'),
    path('change_status/<int:order_id>/', change_order_status, name='change_order_status'),
]

