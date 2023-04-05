from cProfile import label
from django import forms
from .models import Users

# class Regform(forms.Form):
#     U_name = forms.CharField(label='Name')
#     U_dob = forms.DateField(label='Date of Birth')
#     U_username = forms.CharField(label='Username')
#     U_password = forms.CharField(label='Password')

class Regform(forms.ModelForm):
    class Meta:
        model = Users
        fields=['U_name','U_dob','U_username','U_password']
        labels={'U_name':'Name','U_dob':'Date of Birth','U_username':'Username','U_password':'Password'}
        widgets={
            'U_dob':forms.widgets.DateInput(attrs={'type':'date'}),
            'U_password': forms.PasswordInput,
            'U_re_password':forms.PasswordInput,
        }
    U_repassword = forms.CharField(label='Enter Password Again', widget= forms.PasswordInput)