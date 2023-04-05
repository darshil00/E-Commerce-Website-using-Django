from operator import mod
from django.db import models

class Users(models.Model):
    U_name=models.CharField(max_length=10)
    U_dob=models.DateField()
    U_username=models.CharField(max_length=30)
    U_password=models.CharField(max_length=20)
    def __str__(self):
        return self.U_name

class Products(models.Model):
    image=models.ImageField(upload_to='images/')
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Cart(models.Model):
    C_users=models.ForeignKey(Users, on_delete=models.CASCADE, related_name="CartUsers")
    C_products=models.ForeignKey(Products ,on_delete=models.CASCADE, related_name="CartProducts")
    C_status=models.IntegerField()
    def __str__(self):
        return self.C_users

class Customer(models.Model):
    email=models.EmailField(max_length=254)
    address=models.CharField(max_length=200)
    address2=models.CharField(max_length=200)
    state=models.CharField(max_length=25)
    city=models.CharField(max_length=25)
    zip=models.IntegerField()
    payment=models.CharField(max_length=15)
    name_card=models.CharField(max_length=40)
    number_card=models.IntegerField()
    exp_card=models.IntegerField()
    cvv_card=models.IntegerField()
    det=models.ForeignKey(Users,on_delete=models.CASCADE, related_name="CustomerOrders")
    def __str__(self):
        return self.name_card

class Orders(models.Model):
    User_details=models.ForeignKey(Users,on_delete=models.CASCADE,related_name="OrdersUsers")
    Purchase_details=models.DateTimeField(auto_now_add=True)
    Order_details=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="OrdersCart")
    Order_number=models.IntegerField()

class number(models.Model):
    select=models.IntegerField()