from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.forms import formset_factory
from typing import List, Dict, Any
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/")

# Форма для добавления товаров в заказ
class OrderItemForm(forms.Form):
    item = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )


def order_list(request) -> JsonResponse:
    """Отображение списка заказов с фильтрацией."""
    # Загрузка статусов через API
    try:
        status_response = requests.get(f'{API_BASE_URL}statuses/', timeout=10)
        status_response.raise_for_status()
        status_choices: List[Dict[str, str]] = status_response.json()
    except requests.RequestException as e:
        messages.error(request, f"Ошибка загрузки статусов: {e}")
        status_choices = []

    # Получение параметров поиска
    table_number: str = request.GET.get('table_number', '')
    status: str = request.GET.get('status', '')
    params: Dict[str, str] = {}
    if table_number:
        params['table_number'] = table_number
    if status:
        params['status'] = status

    # Загрузка заказов через API
    try:
        response = requests.get(f'{API_BASE_URL}orders/', params=params, timeout=10)
        response.raise_for_status()
        orders: List[Dict[str, Any]] = response.json()
    except requests.RequestException as e:
        messages.error(request, f"Ошибка загрузки заказов: {e}")
        orders = []

    # Отображение страницы с данными
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_choices': status_choices,
        'current_table_number': table_number,
        'current_status': status,
    })


def add_order(request) -> JsonResponse:
    """Добавление нового заказа."""
    # Получение списка товаров из API
    try:
        response = requests.get(f'{API_BASE_URL}items/', timeout=10)
        response.raise_for_status()
        items: List[Dict[str, str]] = response.json()

        # Формируем выбор для выпадающего списка
        item_choices = [(item['id'], item['name']) for item in items]
    except requests.RequestException as e:
        messages.error(request, f"Ошибка загрузки товаров: {e}")
        item_choices = []

    # Устанавливаем выбор товаров для формы
    OrderItemForm.base_fields['item'].choices = item_choices

    # Создаем FormSet для позиций заказа
    OrderItemFormSet = formset_factory(OrderItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST)

        # Получение номера стола
        table_number: str = request.POST.get('table_number', '')

        if formset.is_valid():
            # Проверка номера стола
            if not table_number:
                messages.error(request, "Пожалуйста, укажите номер стола.")
                return render(request, 'orders/add_order.html', {'formset': formset})

            # Собираем данные для отправки на API
            order_data: Dict[str, Any] = {
                'table_number': table_number,
                'status': 'pending',
                'items': [
                    {'item': form.cleaned_data['item'], 'quantity': form.cleaned_data['quantity']}
                    for form in formset if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                ]
            }

            try:
                # Отправляем данные на API
                response = requests.post(f'{API_BASE_URL}orders/', json=order_data, timeout=10)
                response.raise_for_status()
                messages.success(request, 'Заказ успешно создан.')
                return redirect('order_list')
            except requests.RequestException as e:
                messages.error(request, f"Ошибка создания заказа: {e}")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")

    else:
        formset = OrderItemFormSet()

    return render(request, 'orders/add_order.html', {
        'formset': formset,
    })


def delete_order(request, order_id: int) -> JsonResponse:
    """Удаление заказа."""
    try:
        response = requests.delete(f'{API_BASE_URL}orders/{order_id}/', timeout=10)
        response.raise_for_status()
        messages.success(request, 'Заказ успешно удалён.')
    except requests.RequestException as e:
        messages.error(request, f"Ошибка при удалении заказа: {e}")
    return redirect('order_list')


def change_order_status(request, order_id: int) -> JsonResponse:
    """Изменение статуса заказа."""
    if request.method == 'POST':
        new_status: str = request.POST.get('status', '')
        payload: Dict[str, str] = {'status': new_status}

        try:
            response = requests.patch(f'{API_BASE_URL}orders/{order_id}/', json=payload, timeout=10)
            response.raise_for_status()
            messages.success(request, 'Статус заказа успешно обновлён.')
            return redirect('order_list')  # Убедитесь, что маршрут `order_list` существует
        except requests.RequestException as e:
            messages.error(request, f"Ошибка при обновлении статуса: {e}")
            return redirect('order_list')
    return redirect('order_list')


def revenue(request) -> JsonResponse:
    """Отображение общей выручки."""
    try:
        # Запрашиваем только заказы со статусом 'paid'
        response = requests.get(f'{API_BASE_URL}orders/', params={'status': 'paid'}, timeout=10)
        response.raise_for_status()
        orders: List[Dict[str, Any]] = response.json()

        # Суммируем только оплаченные заказы
        total_revenue: float = sum(
            float(order.get('total_price', 0)) for order in orders if order.get('status') == 'paid'
        )
    except requests.RequestException as e:
        messages.error(request, f"Ошибка при получении выручки: {e}")
        total_revenue = 0
    except ValueError as e:
        messages.error(request, f"Ошибка преобразования данных: {e}")
        total_revenue = 0

    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})

