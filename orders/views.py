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
from .forms import ItemForm, OrderForm
from .models import Order, Item



def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'orders/add_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'orders/item_list.html', {'items': items})

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/add_order.html', {'form': form})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})