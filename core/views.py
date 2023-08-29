from django.shortcuts import render
from products.models import Item

def frontpage(request):
    items = Item.objects.filter(status=Item.ACTIVE)
    return render(request, 'core/frontpage.html', {
        'items': items
    })

def about(request):
    return render(request, 'core/about.html')