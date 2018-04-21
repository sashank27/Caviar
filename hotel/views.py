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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from reportlab.pdfgen import canvas
from .models import Customer, Comment, Order, Food, Data, Cart, OrderContent, Staff, DeliveryBoy
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.username = user.email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = form.cleaned_data['address']
            contact = form.cleaned_data['contact']
            customer = Customer.objects.create(customer=user, address=address, contact=contact)
            customer.save()
            return redirect('http://localhost:8000/accounts/login/')
        
    else:
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@staff_member_required
def dashboard_admin(request):
    comments = Comment.objects.count()
    orders = Order.objects.count()
    customers = Customer.objects.count()
    completed_orders = Order.objects.filter(payment_status="Completed")
    top_customers = Customer.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
    datas = Data.objects.filter().order_by('date')
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
    return render(request, 'admin_temp/index.html', context)

@login_required
@staff_member_required
def users_admin(request):
    customers = Customer.objects.filter()
    print(customers)
    return render(request, 'admin_temp/users.html', {'users':customers})

@login_required
@staff_member_required
def orders_admin(request):
    orders = Order.objects.filter()
    dBoys = Staff.objects.filter(role='Delivery Boy')
    print(dBoys)
    return render(request, 'admin_temp/orders.html', {'orders':orders, 'dBoys':dBoys})

@login_required
@staff_member_required
def foods_admin(request):
    foods = Food.objects.filter()
    return render(request, 'admin_temp/foods.html', {'foods':foods})

@login_required
@staff_member_required
def sales_admin(request):
    sales = Data.objects.filter()
    return render(request, 'admin_temp/sales.html', {'sales':sales})

def menu(request):
    cuisine = request.GET.get('cuisine')
    print(cuisine)
    if cuisine is not None:
        if ((cuisine == "Gujarati") or (cuisine == "Punjabi")):
            foods = Food.objects.filter(status="Enabled", course=cuisine)
        elif(cuisine == "south"):
            foods = Food.objects.filter(status="Enabled", course="South Indian")
        elif(cuisine == "fast"):
            foods = Food.objects.filter(course="Fast")
    else:
        foods = Food.objects.filter()
    return render(request, 'menu.html', {'foods':foods, 'cuisine':cuisine})


def index(request):
    food = Food.objects.filter().order_by('-num_order')
    return render(request, 'index.html', {'food':food})


@login_required
@staff_member_required
def confirm_order(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmOrder()
    order.save()
    customerID = order.customer.id
    customer = Customer.objects.get(id=customerID)
    customer.total_sale += order.total_amount
    customer.orders += 1
    customer.save()
    return redirect('hotel:orders_admin')

@login_required
@staff_member_required
def confirm_delivery(request, orderID):
    to_email = []
    order = Order.objects.get(id=orderID)
    order.confirmDelivery()
    order.save()
    mail_subject = 'Order Delivered successfully'
    to = str(order.customer.customer.email)
    to_email.append(to)
    from_email = 'pradeepgangwar39@gmail.com'
    message = "Hi "+order.customer.customer.first_name+" Your order was delivered successfully. Please go to your dashboard to see your order history. <br> Your order id is "+orderID+". Share ypour feedback woth us."
    send_mail(
        mail_subject,
        message,
        from_email,
        to_email,
    )
    return redirect('hotel:orders_admin')

@login_required
@staff_member_required
def edit_food(request, foodID):
    food = Food.objects.filter(id=foodID)[0]
    if request.method == "POST":
        if request.POST['base_price'] != "":
            food.base_price = request.POST['base_price']
        
        if request.POST['discount'] != "":
            food.discount = request.POST['discount'] 
        
        food.sale_price = (100 - float(food.discount))*float(food.base_price)/100

        status = request.POST.get('disabled')
        print(status)
        if status == 'on':
            food.status = "Disabled"
        else:
            food.status = "Enabled"
        
        food.save()
    return redirect('hotel:foods_admin')

@login_required
@staff_member_required
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
        
        if (first_name == "") or (last_name == "") or (address == "") or (contact == "") or (email == "") or (password == "") or (confirm_pass == ""):
            customers = Customer.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/users.html', {'users': customers, 'error_msg': error_msg})

        if password == confirm_pass:
            user = User.objects.create(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            cust = Customer.objects.create(customer=user, address=address, contact=contact)
            cust.save()
            success_msg = "New user successfully created"
            customers = Customer.objects.filter()
            return render(request, 'admin_temp/users.html', {'users': customers, 'success_msg': success_msg})

    return redirect('hotel:users_admin')

@login_required
@staff_member_required
def add_food(request):
    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        status = request.POST['status']
        content = request.POST['content']
        base_price = request.POST['base_price']
        discount = request.POST['discount']
        sale_price = (100 - float(discount)) * float(base_price) / 100
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        if (name == "") or (course is None) or (status is None) or (content == "") or (base_price == "") or (discount == ""):
            foods = Food.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/foods.html', {'foods': foods, 'error_msg': error_msg})

        food = Food.objects.create(name=name, course=course, status=status, content_description=content, base_price=base_price, discount=discount, sale_price=sale_price, image=filename)
        food.save()
        foods = Food.objects.filter()
        success_msg = "Please enter valid details"
        return render(request, 'admin_temp/foods.html', {'foods': foods, 'success_msg': success_msg})
    return redirect('hotel:foods_admin')

@login_required
@staff_member_required
def add_deliveryBoy(request, orderID):
    order = Order.objects.get(id=orderID)
    dName = request.POST['deliveryBoy']
    print(dName)
    user = User.objects.get(first_name=dName)
    deliveryBoy = Staff.objects.get(staff_id=user)
    order.delivery_boy = deliveryBoy
    order.save()
    return redirect('hotel:orders_admin')

@login_required
@staff_member_required
def add_sales(request):
    if request.method == "POST":
        date = request.POST['date']
        sales = request.POST['sales']
        expenses = request.POST['expenses']
        
        if (date is None) or (sales == "") or (expenses == ""):
            sales = Data.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/sales.html', {'sales': sales, 'error_msg': error_msg})

        data = Data.objects.create(date=date, sales=sales, expenses=expenses)
        data.save()
        datas = Data.objects.filter()
        success_msg = "Sales data added successfully!"
        return render(request, 'admin_temp/sales.html', {'sales': datas, 'success_msg': success_msg})

    return redirect('hotel:foods_admin')

@login_required
@staff_member_required
def edit_sales(request, saleID):
    data = Data.objects.filter(id=saleID)[0]
    if request.method == "POST":
        if request.POST['sales'] != "":
            data.sales = request.POST['sales']
        
        if request.POST['expenses'] != "":
            data.expenses = request.POST['expenses'] 
        
        data.save()
    return redirect('hotel:sales_admin')

@login_required
def food_details(request, foodID):
    food = Food.objects.get(id=foodID)
    return render(request, 'user/single.html', {'food':food})

@login_required
def addTocart(request, foodID, userID):
    food = Food.objects.get(id=foodID)
    user = User.objects.get(id=userID)
    cart = Cart.objects.create(food=food, user=user)
    cart.save()
    return redirect('hotel:cart')

@login_required
def delete_item(request, ID):
    item = Cart.objects.get(id=ID)
    item.delete()
    return redirect('hotel:cart')

@login_required
def cart(request):
    user = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=user)
    total = 0
    for item in items:
        total += item.food.sale_price
    return render(request, 'cart.html', {'items': items, 'total':total})

@login_required
def placeOrder(request):
    to_email = []
    customer = Customer.objects.get(customer=request.user)
    print(customer.address)
    items = Cart.objects.filter(user=request.user)
    for item in items:
        food = item.food
        order = Order.objects.create(customer=customer, order_timestamp=timezone.now(), payment_status="Pending", 
        delivery_status="Pending", total_amount=food.sale_price, payment_method="Cash On Delivery", location=customer.address)
        order.save()
        orderContent = OrderContent(food=food, order=order)
        orderContent.save()
        item.delete()
    mail_subject = 'Order Placed successfully'
    to = str(customer.customer.email)
    to_email.append(to)
    from_email = 'pradeepgangwar39@gmail.com'
    message = "Hi "+customer.customer.first_name+" Your order was placed successfully. Please go to your dashboard to see your order history. <br> Your order id is "+order.id+""
    send_mail(
        mail_subject,
        message,
        from_email,
        to_email,
    )
    return redirect('hotel:cart')

@login_required
def my_orders(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(customer=user)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'orders.html', {'orders': orders})

@login_required
def delivery_boy(request):
    user = User.objects.get(id=request.user.id)
    try:
        customer = Customer.objects.get(customer=user)
    except Customer.DoesNotExist:
        staff = Staff.objects.get(staff_id=user)
        if staff is None or staff.role != 'Delivery Boy':
            redirect('hotel:index')
        else:
            orders = DeliveryBoy.objects.filter(delivery_boy=staff)
            return render(request, 'delivery_boy.html', {'orders':orders})
    
    return redirect('hotel:index')
        
