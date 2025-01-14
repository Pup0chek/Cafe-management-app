# orders/forms.py
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    table_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер стола'})
    )
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['table_number', 'status']
