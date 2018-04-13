from django.contrib import admin
from .models import Customer, Staff, Order, Food, Comment, Data

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(Food)
admin.site.register(Comment)
admin.site.register(Data)