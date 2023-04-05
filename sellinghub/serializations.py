from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import Products,Users,Cart,Customer,Orders,number

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields= ('id','image','name','price','description')