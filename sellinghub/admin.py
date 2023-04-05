from django.contrib import admin
from .models import Products, Users, Customer, Cart, Orders
# Register your models here.

admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Customer)