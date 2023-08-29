from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify


from .models import Userprofile

from products.forms import ItemForm
from products.models import Category, Item, Order, OrderItem


# Create your views here
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    items = user.items.filter(status=Item.ACTIVE)

    return render(request, 'users/vendor_detail.html', {
        'user': user,
        'items': items
    })

@login_required
def myitems(request):  
    items = request.user.items.exclude(status=Item.DELETED)
    order_items = OrderItem.objects.filter(item__user=request.user)

    return render(request, 'users/myitems.html', {
        'items': items,
        'order_items': order_items
    })

@login_required
def myitems_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'users/myitems_order_detail.html', {
        'order': order
    })
    
@login_required
def add_item(request):
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = request.POST.get('title')
            item = form.save(commit=False)
            item.user = request.user
            item.slug = slugify(title)
            item.save()
            messages.success(request, 'Item has been added')
            return redirect('myitems')
        
    
    else:
        
        form = ItemForm()

    return render(request, 'users/item_form.html', {
        'title' : 'Add Item',
        'form': form
    })

@login_required
def edit_item(request, pk):
    item = Item.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been edited')
            return redirect('myitems')

    else:
        form = ItemForm(instance=item)

    return render(request, 'users/item_form.html', {
        'title' : 'Edit Item',
        'item' : item,
        'form' : form
    })
@login_required
def delete_item(request, pk):
    item = Item.objects.filter(user=request.user).get(pk=pk)
    item.status = Item.DELETED
    item.save()
    messages.success(request, 'Item has been set to Deleted')

    return redirect('myitems')


@login_required
def myaccount(request):
    return render(request, 'users/myaccount.html')

def signup(request):
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            
            user= form.save()
            
            login(request, user)

            user = Userprofile.objects.create(user=user)
           
            return redirect('myaccount')
    else:
        
        form = UserCreationForm()
    
    return render(request, 'users/sign_up.html', {
        'form': form
    })


