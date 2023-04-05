from django import forms
from .models import Users

class Logform(forms.ModelForm):
    class Meta:
        model = Users
        fields=['U_username','U_password']
        labels={'U_username':'Username','U_password':'Password'}
        widgets={
            'U_password': forms.PasswordInput
        }
