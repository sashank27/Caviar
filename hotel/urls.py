from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^users/$', views.users, name='users'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^foods/$', views.foods, name='foods'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^add_food/$', views.add_food, name='add_food'),
    url(r'^confirm_order/(?P<orderID>\d+)/$', views.confirm_order, name='confirm_order'),
    url(r'^confirm_delivery/(?P<orderID>\d+)/$', views.confirm_delivery, name='confirm_delivery'),
    url(r'^editFood/(?P<foodID>\d+)/$', views.edit_food, name='edit_food'),
]
