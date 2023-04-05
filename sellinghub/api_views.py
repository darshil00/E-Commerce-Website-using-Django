from ast import arg
from cgitb import lookup
from itertools import product
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializations import ProductSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Products
from sellinghub import serializations

class ProductsPagination(LimitOffsetPagination):
    default_limit=10
    max_limit=100

class ProductList(ListAPIView):
    queryset=Products.objects.all()
    serializer_class=ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id',)
    search_fields = ('name','description')
    pagination_class = ProductsPagination

class ProductCreate(CreateAPIView):
    serializer_class=ProductSerializer
    def create(self,request,*args, **kwargs):
        try:
            price=request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({'price': 'must be above 0.0'})
        except ValueError:
            raise ValidationError({'price' 'a valid number is required'})
        return super().create(request, *args, **kwargs)

class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset =Products.objects.all()
    lookup_field = 'id'
    serializer_class= ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id=request.data.get('id')
        response=super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(product_id))
        return response
    
    def update(self, request, *args, **kwargs):
        response=super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product=response.data
            cache.set('product_data_{}'.format(product['id']),{
                'name': product['name'],
                'description': product['description'],
                'image':product['image'],
                'price':product['price'],
            })
        return response
    