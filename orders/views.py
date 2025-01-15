from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.db.models import Sum
from django import forms
from .models import Order, OrderItem
from .forms import OrderForm


def add_order(request):
    OrderItemFormSet = inlineformset_factory(
        Order, OrderItem,
        fields=('item', 'quantity'),
        extra=1,
        can_delete=True,
        widgets={
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Сохраняем объект Order
            order = form.save()

            # Устанавливаем связь с Order для formset и сохраняем formset
            formset.instance = order
            formset.save()

            # Теперь вызываем calculate_total_price
            order.calculate_total_price()
            order.save()  # Сохраняем изменения после обновления total_price

            messages.success(request, 'Заказ успешно создан.')
            return redirect('order_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/add_order.html', {'form': form, 'formset': formset})



def order_list(request):
    # Получение параметров фильтрации из GET-запроса
    table_number = request.GET.get('table_number')
    status = request.GET.get('status')

    # Начальное множество заказов
    orders = Order.objects.all()

    # Применение фильтрации, если параметры заданы
    if table_number:
        orders = orders.filter(table_number=table_number)
    if status:
        orders = orders.filter(status=status)

    # Получение всех доступных статусов для выпадающего списка
    STATUS_CHOICES = Order.STATUS_CHOICES

    context = {
        'orders': orders,
        'status_choices': STATUS_CHOICES,
        'current_table_number': table_number or '',
        'current_status': status or '',
    }
    return render(request, 'orders/order_list.html', context)


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        try:
            order.delete()
            messages.success(request, 'Заказ успешно удалён.')
        except Exception as e:
            messages.error(request, 'Ошибка при удалении заказа.')
    return redirect('order_list')


def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'Статус заказа успешно обновлён.')
        else:
            messages.error(request, 'Некорректный статус.')
    return redirect('order_list')


def revenue(request):
    total_revenue = Order.objects.filter(status='paid').aggregate(total=Sum('total_price'))['total'] or 0
    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})
