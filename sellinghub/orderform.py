from django import forms
from .models import Customer

class Orderform(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['email','address','address2','state','city','zip','payment','name_card','number_card','exp_card','cvv_card']
        labels={'email':'Email','address':'Address','address2':'Address 2','state':'State','city':'City','zip':'Zip','payment':'Payment','name_card':'Name on Card','number_card':'Number','exp_card':'Expiration','cvv_card':'CVV'}