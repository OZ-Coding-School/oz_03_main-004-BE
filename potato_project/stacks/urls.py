from django.urls import path

from . import views

urlpatterns = [
    path("", views.StackList.as_view(), name="stack_list")
]