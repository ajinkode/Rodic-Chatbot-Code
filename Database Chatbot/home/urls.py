from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('',views.index,name='home'),
    path('index',views.index,name='home'),
    # path('function',views.function)
]