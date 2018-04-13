from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^users/$', views.users, name='users'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^menu/$', views.menu, name='menu'),
]
