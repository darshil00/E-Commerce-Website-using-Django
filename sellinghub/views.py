from django.http import HttpResponseRedirect
import xml.etree.ElementTree as ET
from .table import SimpleTable
import openpyxl
import sqlite3 as my
from django.urls import reverse
from django.contrib import messages
from .regform import Regform
from .number import Number
from .orderform import Orderform
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Products,Users,Cart,Customer,Orders,number
from .loginform import Logform
from django.shortcuts import render, redirect
from datetime import datetime
import django_tables2 as tables

def logout(request):
    response = redirect('login')
    response.delete_cookie('USERID')
    return response

def login(request):
    user=Users.objects.all()
    filled_form = Logform(request.POST)
    if filled_form.is_valid():
        for i in user:
            if i.U_username == filled_form.cleaned_data.get('U_username') and i.U_password == filled_form.cleaned_data.get('U_password'):
                ids=i.id
                response = redirect(reverse('display'))
                response.set_cookie('USERID', ids)  
                return response
        messages.info(request, 'USERNAME OR PASSWORD INCORRECT !!')
        return render(request, 'hub/login.html', {'user':user, 'logform':filled_form})
    return render(request, 'hub/login.html', {'logform':filled_form, 'user':user})
    
def register(request):
    created_reg_pk = None
    filled_form = Regform(request.POST)
    if filled_form.is_valid():
        password =filled_form.cleaned_data.get('U_password')
        repass=filled_form.cleaned_data.get('U_repassword')
        print(repass)
        if password == repass:
            created_reg = filled_form.save()
            created_reg_pk = created_reg.id
            filled_form = Regform()
            messages.info(request, 'Your Account has been created successfully!')
        else:
            messages.info(request, 'PASSWORDS DONT MATCH')
            return render(request, 'hub/register.html',{'regform':filled_form})
    return render(request, 'hub/register.html', {'regform':filled_form, 'created_reg_pk':created_reg_pk})

def display(request):   
    user = request.COOKIES['USERID']  
    product=Products.objects.all()  
    return render(request, 'hub/display.html', {'product':product, 'userid':user})

def checkout(request):
    user = request.COOKIES['USERID']
    user=int(user)  
    filled_form = Orderform(request.POST)
    product=Products.objects.all()
    User=Users.objects.all()
    CartData=Cart.objects.all()
    customer=Customer.objects.all()
    items=0
    if request.method=="POST":
        if request.POST.get('remove_button'):
            a= int(request.POST.get('remove_button'))
            CartData.filter(id=a).delete()
        filled_form = Orderform(request.POST)
        if filled_form.is_valid():
            new=Customer(det_id=user,email=filled_form.cleaned_data.get('email'),address=filled_form.cleaned_data.get('address'),address2=filled_form.cleaned_data.get('address2'),state=filled_form.cleaned_data.get('state'),city=filled_form.cleaned_data.get('city'),zip=filled_form.cleaned_data.get('zip'),payment=filled_form.cleaned_data.get('payment'),name_card=filled_form.cleaned_data.get('name_card'),number_card=filled_form.cleaned_data.get('number_card'),exp_card=filled_form.cleaned_data.get('exp_card'),cvv_card=filled_form.cleaned_data.get('cvv_card'))
            new.save()
            filled_form = Orderform()
            for k in customer:
                order_num=k.id
            for i in User:
                if i.id==user:
                    for j in CartData:
                        if j.C_users_id == user:
                            if j.C_status==0:
                                ord=Orders(Order_details_id=j.id,User_details_id=i.id,Order_number=order_num)
                                ord.save()
                                new=Cart.objects.filter(C_users_id=user).update(C_status=1)
            return redirect(reverse('display'))
    for i in User:
        if i.id == user:
            names=[]
            cost=[]
            ids=[]
            stats=[]
            for j in CartData:
                if j.C_users_id == user:
                    for k in product:
                        if j.C_products_id==k.id:
                            if j.C_status==0:
                                items=items+1
                                stats.append(j.C_status)
                                ids.append(j.id)
                                names.append(k.name)
                                cost.append(k.price)
            total=sum(cost)
            zipped_data= zip(names,cost,ids,stats)
            return render(request, 'hub/checkout.html', {'product':product, 'userid':user, 'zipped_data':zipped_data, 'total':total, 'items':items,'orderform':filled_form})
    return render(request, 'hub/checkout.html', {'product':product, 'userid':user,'orderform':filled_form})

def details(request, pr_id):
    product= get_object_or_404(Products,pk=pr_id)
    user = request.COOKIES['USERID']
    user=int(user)  
    if request.method=="POST":
        if (request.POST.get('button1', False)):
            new = Cart(C_products_id=product.id,C_users_id=user,C_status=0)
            new.save()
    return render(request,'hub/details.html',{
        'product':product,'user':user,
    })

def orderlist(request):
    user = request.COOKIES['USERID']
    user=int(user)
    total=[]
    order_numbers=[]
    orders=Orders.objects.all()
    total_orders=Orders.objects.values('Order_number').distinct().count()
    for i in range(total_orders):
        total.append(i+1)
    for i in orders:
        if i.User_details_id == user:
            test=order_numbers.count(i.Order_number)
            if test<=0:
                order_numbers.append(i.Order_number)
    zipped_data=zip(total,order_numbers)
    return render(request, 'hub/orderlist.html',{'zipped_data':zipped_data})

def orders(request,or_id):
    ORDER = get_list_or_404(Orders,Order_number=or_id)
    user = request.COOKIES['USERID']
    user=int(user)
    order=Orders.objects.all()
    carts=Cart.objects.all()
    products=Products.objects.all()
    Names=[]
    Prices=[]
    Time=[]
    for i in order:
        if i.User_details_id==user:
            if i.Order_number == or_id:
                for j in carts:
                    if i.Order_details_id == j.id:
                        for k in products:
                            if j.C_products_id == k.id:
                                Names.append(k.name)
                                Prices.append(k.price)
                                Time.append(i.Purchase_details)
                                zipped_data= zip(Names,Prices,Time)
    return render(request, 'hub/orders.html',{'zipped_data':zipped_data})

def addexcel(request):
    if "GET" == request.method:
        return render(request, 'hub/addexcel.html')
    else:
        try:
            database = my.connect("db.sqlite3")
            cur=database.cursor()
            print("CONNECTED")
        except:
            print("error")
        excel_file = request.FILES["excel_file"]
        names=[]
        data=[]
        wb = openpyxl.load_workbook(excel_file)
        sheet=wb.active
        for rows in sheet.iter_rows(min_row=2,min_col=1):
            sql="SELECT U_name,U_dob,U_username,U_password from sellinghub_users WHERE (sellinghub_users.U_name = '{}') and (sellinghub_users.U_dob = '{}') and (sellinghub_users.U_username = '{}') and (sellinghub_users.U_password = '{}');".format(rows[0].value,rows[1].value.date(),rows[2].value,rows[3].value)
            cur.execute(sql)
            names=cur.fetchall()
            if not names:
                new=Users(U_name=rows[0].value,U_dob=rows[1].value.date(),U_username=rows[2].value,U_password=rows[3].value)
                new.save()
            else:
                data.append(names)
        return render(request, 'hub/addexcel.html',{'excel_data':data})

def addxml(request):
    if "GET" == request.method:
        return render(request, 'hub/addxml.html')
    else:
        try:
            database = my.connect("db.sqlite3")
            cur=database.cursor()
            print("CONNECTED")
        except:
            print("error")
        data=[]
        xml_file = request.FILES["xml_file"]
        tree = ET.parse(xml_file)
        root=tree.getroot()
        for i in root:
            sql="SELECT U_name,U_dob,U_username,U_password from sellinghub_users WHERE (sellinghub_users.U_name = '{}') and (sellinghub_users.U_dob = '{}') and (sellinghub_users.U_username = '{}') and (sellinghub_users.U_password = '{}');".format(i[0].text,i[1].text,i[2].text,i[3].text)
            cur.execute(sql)
            names=cur.fetchall()
            if not names:
                new=Users(U_name=i[0].text,U_dob=i[1].text,U_username=i[2].text,U_password=i[3].text)
                new.save()
            else:
                data.append(names)
        return render(request, 'hub/addxml.html',{'xml_data':data})

def viewtable(request):
    num = number.objects.all()
    for i in num:
        size=i.select
    queryset = Users.objects.all()
    table = SimpleTable(Users.objects.all())
    filled_form = Number(request.POST)
    if request.method == "POST":
        if filled_form.is_valid():
            a=filled_form.cleaned_data['select']
            table.paginate(page=request.GET.get("page", 1), per_page=a)
            new=number(id=1,select=a)
            new.save()
            return render(request, 'hub/viewtable.html',{'query':queryset,'table':table,'form':filled_form})
    table.paginate(page=request.GET.get("page", 1), per_page=size)
    return render(request, 'hub/viewtable.html',{'query':queryset,'table':table,'form':filled_form})
