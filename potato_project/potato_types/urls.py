from django.urls import path

from . import views

urlpatterns = [
    path("", views.PotatoesList.as_view(), name="potatoes-list"),
]
