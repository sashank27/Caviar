from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from reportlab.pdfgen import canvas
from .models import Customer, Comment, Order, Food, Data

# Create your views here.
def index(request):
    comments = Comment.objects.count()
    orders = Order.objects.count()
    customers = Customer.objects.count()
    completed_orders = Order.objects.filter(payment_status="Completed")
    top_customers = Customer.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
    datas = Data.objects.filter()
    sales = 0
    for order in completed_orders:
        sales += order.total_amount

    context = {
        'comments':comments,
        'orders':orders,
        'customers':customers,
        'sales':sales,
        'top_customers': top_customers,
        'latest_orders':latest_orders,
        'datas':datas,
    }
    return render(request, 'index.html', context)

def menu(request):
    foods = Food.objects.filter()
    return render(request, 'menu.html', {'foods':foods})

def signup(request):
    return render(request, 'registration/signup.html')

def users(request):
    customers = Customer.objects.filter()
    print(customers)
    return render(request, 'users.html', {'users':customers})

def orders(request):
    orders = Order.objects.filter()
    return render(request, 'orders.html', {'orders':orders})

def foods(request):
    foods = Food.objects.filter()
    return render(request, 'foods.html', {'foods':foods})

def confirm_order(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmOrder()
    order.save()
    customerID = order.customer.id
    customer = Customer.objects.get(id=customerID)
    customer.total_sale += order.total_amount
    customer.orders += 1
    customer.save()
    return redirect('hotel:orders')

def confirm_delivery(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmDelivery()
    order.save()
    return redirect('hotel:orders')
def edit_food(request, foodID):
    food = Food.objects.filter(id=foodID)[0]
    if request.method == "POST":
        if request.POST['base_price'] != "":
            food.base_price = request.POST['base_price']
        
        if request.POST['discount'] != "":
            food.discount = request.POST['discount'] 
        
        # print(request.POST['base_price'])

        food.sale_price = (100 - float(food.discount))*float(food.base_price)/100

        status = request.POST.get('disabled')
        print(status)
        if status == 'on':
            food.status = "Disabled"
        else:
            food.status = "Enabled"
            # print(food.status)
        food.save()
    return redirect('hotel:foods')

def add_user(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        contact = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pass = request.POST['confirm_password']
        username = email.split('@')[0]
        print(last_name)

        if (first_name == "") or (last_name == "") or (address == "") or (contact == "") or (email == "") or (password == "") or (confirm_pass == ""):
            customers = Customer.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'users.html', {'users': customers, 'error_msg': error_msg})

        if password == confirm_pass:
            user = User.objects.create(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            cust = Customer.objects.create(customer=user, address=address, contact=contact)
            cust.save()
            success_msg = "New user successfully created"
            customers = Customer.objects.filter()
            return render(request, 'users.html', {'users': customers, 'success_msg': success_msg})
    return redirect('hotel:users')

def add_food(request):
    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        status = request.POST['status']
        content = request.POST['content']
        base_price = request.POST['base_price']
        discount = request.POST['discount']
        sale_price = (100 - float(discount)) * float(base_price) / 100
        print(sale_price)

        if (name == "") or (course is None) or (status is None) or (content == "") or (base_price == "") or (discount == ""):
            foods = Food.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'foods.html', {'foods': foods, 'error_msg': error_msg})

        food = Food.objects.create(name=name, course=course, status=status, content_description=content, base_price=base_price, discount=discount, sale_price=sale_price)
        food.save()
        foods = Food.objects.filter()
        success_msg = "Please enter valid details"
        return render(request, 'foods.html', {'foods': foods, 'success_msg': success_msg})
    return redirect('hotel:foods')