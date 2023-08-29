from django import forms

from .models import Item, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address',)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'title', 'description', 'image', 'price',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-400'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-400'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-400'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-2 border border-gray-400'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-400'
            }),
        }