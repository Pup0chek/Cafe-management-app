from django.db import models
from django.db.models import Sum, F
from django.core.exceptions import ValidationError


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    table_number = models.IntegerField()
    items = models.ManyToManyField('Item', through='OrderItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('paid', 'Paid'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def calculate_total_price(self):
        """Вычисляет и обновляет общую стоимость заказа."""
        total = self.orderitem_set.aggregate(
            total=Sum(F('item__price') * F('quantity'))
        )['total'] or 0
        self.total_price = total

    def clean(self):
        """Ensure the order has at least one item."""
        if not self.pk:
            # Первичный ключ еще не создан, пропускаем проверку
            return
        if not self.orderitem_set.exists():
            raise ValidationError("Order must contain at least one item.")

    def save(self, *args, **kwargs):
        # Сначала сохраняем заказ, чтобы был создан первичный ключ
        super().save(*args, **kwargs)

        # Пересчитываем общую стоимость
        self.calculate_total_price()

        # Сохраняем снова после обновления цены
        super().save(update_fields=['total_price'], *args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitem_set', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'item')

    def __str__(self):
        return f"{self.item} x {self.quantity} (Order {self.order.id})"
