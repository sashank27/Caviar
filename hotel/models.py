from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    pending = 'Pending'
    verified = 'Verified'

    STATUS = (
        (pending,pending),
        (verified,verified),
    )

    cust = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    date_registered = models.DateTimeField(auto_now=timezone.now())
    status = models.CharField(max_length=20, choices = STATUS, default = pending)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)
    
    def __str__(self):
        return self.cust.first_name + " " + self.cust.last_name

class Staff(models.Model):
    admin = 'Admin'
    deliveryboy = 'Delivery Boy'
    chef = 'Chef'

    ROLES = (
        (admin,admin),
        (chef,chef),
        (deliveryboy,deliveryboy),
    )
    
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = User.first_name
    last_name = User.last_name
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    email = User.email
    salary = models.IntegerField()
    role = models.CharField(max_length = 30, choices = ROLES)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Order(models.Model):
    pending = 'Pending'
    process = 'Processing'
    completed = 'Completed'

    STATUS = (
        (pending,pending),
        (process,process),
        (completed,completed),
    )

    cod = 'Cash On Delivery'
    card = 'Card Payment'
    upi = 'UPI Payment'

    PAYMENT = (
        (cod,cod),
        (card,card),
        (upi,upi),
    )
    
    #order_id = 
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(blank=True)
    delivery_timestamp = models.DateTimeField(blank=True)
    payment_status = models.CharField(max_length = 30, choices = STATUS)
    delivery_status = models.CharField(max_length = 30, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length = 30, choices = PAYMENT)

    def confirmOrder(self):
        self.order_timestamp = timezone.now()
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.now()
        self.save()

class Food(models.Model):
    indian = 'Indian'
    chinese = 'Chinese'
    continental = 'Continental'
    
    COURSE = (
        (indian,indian),
        (chinese,chinese),
        (continental,continental),
    )

    #food_id
    course = models.CharField(max_length = 50, choices = COURSE)
    content_description = models.TextField()
    base_price = models.FloatField()
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    
    #sale_price = (100.0 - float(discount))/100.0 * float(base_price)
