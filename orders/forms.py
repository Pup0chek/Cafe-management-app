from django import forms
from .models import Order
import json

class OrderForm(forms.ModelForm):
    # Поле для ввода блюд в виде JSON
    items = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        help_text='Введите блюда в формате JSON. Пример: [{"name": "Пицца", "price": 250}, {"name": "Кофе", "price": 100}]'
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES)
        }

    def clean_items(self):
        data = self.cleaned_data['items']
        try:
            items = json.loads(data)
            if not isinstance(items, list):
                raise forms.ValidationError("Блюда должны быть списком.")
            for item in items:
                if 'name' not in item or 'price' not in item:
                    raise forms.ValidationError("Каждое блюдо должно содержать 'name' и 'price'.")
                if not isinstance(item['price'], (int, float)) or item['price'] < 0:
                    raise forms.ValidationError("'price' должно быть положительным числом.")
            return items
        except json.JSONDecodeError:
            raise forms.ValidationError("Неверный формат JSON.")
