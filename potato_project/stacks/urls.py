from django.urls import path

from . import views

urlpatterns = [path("", views.UserStackList.as_view(), name="stack_list")]
