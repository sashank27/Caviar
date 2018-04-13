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
from .models import Customer, Comment, Order

# Create your views here.
def index(request):
    comments = Comment.objects.count()
    orders = Order.objects.count()
    customers = Customer.objects.count()
    completed_orders = Order.objects.filter(delivery_status="Completed")
    top_customers = Customer.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
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
    }
    return render(request, 'index.html', context)

def menu(request):        
    return render(request, 'forms.html')

def signup(request):
    return render(request, 'registration/signup.html')
    return render(request, 'menu.html')

def users(request):
    customers = Customer.objects.filter()
    return render(request, 'tables.html', {'users':customers})

def order(request):
    return render(request, 'order.html')