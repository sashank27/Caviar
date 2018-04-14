from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^users/$', views.users, name='users'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^foods/$', views.foods, name='foods'),
    url(r'^confirm_order/(?P<orderID>\d+)/$', views.confirm_order, name='confirm_order'),
    url(r'^confirm_delivery/(?P<orderID>\d+)/$', views.confirm_delivery, name='confirm_delivery'),
]
