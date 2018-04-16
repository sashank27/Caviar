from django.contrib import admin
from .models import Customer, Staff, Order, Food, Comment, Data, OrderContent, Cart

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(Food)
admin.site.register(Comment)
admin.site.register(Data)
admin.site.register(OrderContent)
admin.site.register(Cart)