
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ItemForm
from .models import Item



def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/add_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})