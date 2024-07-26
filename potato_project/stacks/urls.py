from django.urls import path

from . import views

urlpatterns = [path("all", views.StackList.as_view(), name="stack_list")]
