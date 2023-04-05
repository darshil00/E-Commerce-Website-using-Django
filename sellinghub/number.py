from logging import PlaceHolder
from django import forms
from .models import number

class Number(forms.ModelForm):
    numberchoices=(("2","2"),("3","3"),("5","5"))
    select= forms.ChoiceField(choices=numberchoices, required=False, label="SELECT")
    class Meta:
        model = number
        fields=['select']
        label={'select':'Select'}