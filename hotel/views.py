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
