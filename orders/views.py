import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm
from django.db.models import Sum
from django.contrib import messages

# def order_list(request):
#     search_query = request.GET.get('search', '')
#     filter_status = request.GET.get('status', '')

#     orders = Order.objects.all()

#     if search_query:
#         orders = orders.filter(table_number__icontains=search_query) | orders.filter(status__icontains=search_query)

#     if filter_status:
#         orders = orders.filter(status=filter_status)

#     context = {
#         'orders': orders,
#         'search_query': search_query,
#         'filter_status': filter_status,
#         'status_choices': Order.STATUS_CHOICES,
#     }
#     return render(request, 'orders/order_list.html', context)

# def order_add(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Заказ успешно добавлен!')
#             return redirect('order_list')
#     else:
#         form = OrderForm()
#     return render(request, 'orders/order_form.html', {'form': form, 'title': 'Добавить заказ'})

# def order_edit(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Заказ успешно обновлен!')
#             return redirect('order_list')
#     else:
#         initial_data = {
#             'items': json.dumps(order.items, ensure_ascii=False, indent=4)
#         }
#         form = OrderForm(instance=order, initial=initial_data)
#     return render(request, 'orders/order_form.html', {'form': form, 'title': 'Редактировать заказ'})

# def order_delete(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         order.delete()
#         messages.success(request, 'Заказ успешно удален!')
#         return redirect('order_list')
#     return render(request, 'orders/order_confirm_delete.html', {'order': order})

# def revenue_report(request):
#     revenue = Order.objects.filter(status='paid').aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
#     return render(request, 'orders/revenue_report.html', {'revenue': revenue})

# orders/views.py
from django.shortcuts import render, redirect
from .forms import OrderForm, forms
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, OrderItem
from django.forms import inlineformset_factory
from django.contrib import messages


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
            order = form.save(commit=False)
            # Вычисляем общую стоимость
            total = 0
            for form_item in formset:
                if form_item.cleaned_data and not form_item.cleaned_data.get('DELETE', False):
                    item = form_item.cleaned_data.get('item')
                    quantity = form_item.cleaned_data.get('quantity')
                    total += item.price * quantity
            order.total_price = total
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_list')
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

from django.contrib import messages

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
