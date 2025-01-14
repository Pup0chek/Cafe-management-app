# orders/forms.py
from django import forms
from .models import Item, Order

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в рублях'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'table_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер стола'}),
            'items': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_items(self):
        items = self.cleaned_data.get('items')
        if not items:
            raise forms.ValidationError("Пожалуйста, выберите хотя бы одно блюдо.")
        return items

    def save(self, commit=True):
        # Получаем экземпляр заказа без сохранения в базу данных
        order = super().save(commit=False)

        # Вычисляем общую стоимость на основе выбранных блюд
        total = sum(item.price for item in self.cleaned_data['items'])
        order.total_price = total

        if commit:
            # Сохраняем заказ в базу данных
            order.save()
            # Сохраняем связи ManyToMany (items)
            self.save_m2m()

        return order