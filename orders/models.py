from django.db import models
from django.core.validators import MinValueValidator
import json

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Блюда")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Общая стоимость")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def save(self, *args, **kwargs):
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number}"
