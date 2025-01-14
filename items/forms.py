from django import forms
from .models import Item
from django.forms import inlineformset_factory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в рублях'}),
        }
