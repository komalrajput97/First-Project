from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.forms.widgets import TextInput, EmailInput, PasswordInput, NumberInput

from .models import Order

class OrderPlacingForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name','customer_phone','customer_email','shipping_address','billing_address']
        widgets={
            'customer_name': TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your name'}),
            'customer_phone': TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your number','pattern':'[0-9]+','minlength':10}),
            'customer_email': EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter email'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-textarea'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-textarea'}),
        }
