# orders/models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    table_number = models.IntegerField()
    items = models.ManyToManyField(Item, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Установлено default=0
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"
