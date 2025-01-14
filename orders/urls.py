from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    # path('order/add/', views.order_add, name='order_add'),
    # path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    # path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    # path('revenue/', views.revenue_report, name='revenue_report'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.add_order, name='add_order'),
]