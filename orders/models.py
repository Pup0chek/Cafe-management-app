from django.db import models
from django.db.models import Sum, F
from django.core.exceptions import ValidationError
from typing import List


class Item(models.Model):
    name: str = models.CharField(max_length=100)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    table_number: int = models.IntegerField()
    
    STATUS_CHOICES: List[tuple] = [
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('paid', 'Paid'),
    ]
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self) -> float:
        """Calculate the total price of the order."""
        total: float = self.items.aggregate(
            total=Sum(F('quantity') * F('item__price'))
        )['total'] or 0
        self.total_price = total
        return self.total_price

    def clean(self) -> None:
        """Ensure the order has at least one item."""
        if not self.pk:
            # Skip check for new orders without a primary key
            return
        if not self.items.exists():
            raise ValidationError("Order must contain at least one item.")

    def save(self, *args: tuple, **kwargs: dict) -> None:
        """Override save to ensure total price is updated."""
        super().save(*args, **kwargs)
        if self.pk:  # Ensure the order is already saved
            self.calculate_total_price()
            super().save(update_fields=['total_price'])

    def __str__(self) -> str:
        return f"Order {self.id} - Table {self.table_number}"


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item: Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'item')

    def __str__(self) -> str:
        return f"{self.item} x {self.quantity} (Order {self.order.id})"
