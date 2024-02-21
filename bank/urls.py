from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<str:pk>/pay/', views.payorder, name='pay-order'),
    path('callback/', views.Idpaycallback, name='callback'),
    path('add/order/', views.addorderview, name='order-add'),
]