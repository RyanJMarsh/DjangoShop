from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
import json
import stripe
from .models import Item, Category, Order, OrderItem
from .cart import Cart
from .forms import OrderForm
# Create your views here.


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.items.filter(status=Item.ACTIVE)
    return render(request, 'products/category_detail.html', {
        'category': category,
        'items': items
    })

def item_detail(request, category_slug, slug):

    
    item = get_object_or_404(Item, slug=slug, status=Item.ACTIVE)
    return render(request, 'products/item_detail.html', {
        'item': item
    })

def search(request):
    query=request.GET.get('query', '')
    items = Item.objects.filter(status=Item.ACTIVE).filter(title__icontains=query)

    return render(request, 'products/search.html', {
        'query': query,
        'items': items
    })

@login_required
def add_to_cart(request, item_id):
    cart = Cart(request)
    cart.add(item_id)
    return redirect('cart_view')

def change_quantity(request, item_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(item_id, quantity)

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)

    return render(request, 'products/cart_view.html', {
        'cart': cart
    })

def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(str(item_id))

    return redirect('cart_view')

@login_required
def checkout(request):
    cart = Cart(request)
    

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_cost = 0
            items = []
            

            for item in cart:
               unit_amount = item['total_price'] / item['quantity']
               total_cost += int(item['total_price']) * 100
            
               items.append({
                   'price_data': {
                       'currency': 'gbp',
                       'product_data': {
                           'name': item['item'].title
                       },
                       'unit_amount': int(unit_amount) *100
                   },
                   'quantity': item['quantity']
               })
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items = items,
                mode = 'payment',
                success_url = f'{settings.WEBSITE_URL}cart/success/',
                cancel_url = f'{settings.WEBSITE_URL}cart/'
            )
            payment_intent = stripe.PaymentIntent.create(
                amount= total_cost,
                currency="gbp",
                payment_method_types=["card"],
                )

            order = form.save(commit=False)
            order.created_by = request.user
            order.is_paid = True
            order.payment_intent = payment_intent.id
            order.total_cost = total_cost
            order.save()
            

            for item in cart:
               product = item['item']
               quantity = int(item['quantity'])
               price = int(item['total_price'])

               item = OrderItem.objects.create(order=order, item=product, price=price, quantity=quantity)

            cart.clear()
           
            return redirect(session.url, code=303)
    else:
        form = OrderForm()
    
    return render(request, 'products/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def success(request):
    return render(request, 'products/success.html')