from django.conf import settings
from .models import Item

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['item'] = Item.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['item'].price * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True            

    def add(self, item_id, quantity=1):
        item_id = str(item_id)

        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': int(quantity), 'id': item_id}

        else:
            self.cart[item_id]['quantity'] += int(quantity)

            if self.cart[item_id]['quantity'] == 0:
                self.remove(item_id)

        self.save()

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['item'] = Item.objects.get(pk=p)

        return sum(item['total_price'] for item in self.cart.values())
    
    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True