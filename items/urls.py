# items/urls.py

from django.urls import path
from . import views

app_name = 'items'  # Определение пространства имён

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
]
