from dataclasses import field
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'address1',
            'address2',
            'country',
            'state',
            'city',
            'pincode',
            'order_note',
        ]
    def __init__(self,*args, **kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="form-control"  