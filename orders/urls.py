from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path('order/add/', views.order_add, name='order_add'),
    # path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    # path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    # path('revenue/', views.revenue_report, name='revenue_report'),

    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('revenue/', views.revenue, name='revenue'),
    path('change_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
]

