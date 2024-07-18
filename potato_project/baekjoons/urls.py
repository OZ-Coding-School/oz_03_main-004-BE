# baekjoons/urls.py
from django.urls import path
from .views import profile_view

urlpatterns = [
    path('<str:userid>/scores/', profile_view, name='profile_view'),
]
