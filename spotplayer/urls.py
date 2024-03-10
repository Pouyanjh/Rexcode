
from django.urls import path

from . import views

urlpatterns = [
    path('addspot/', views.addspot, name='spot-add'),
]