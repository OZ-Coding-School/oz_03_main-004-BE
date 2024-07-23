from django.urls import path

from . import views

<<<<<<< HEAD
urlpatterns = [path("", views.UserStackList.as_view(), name="stack_list")]
=======
urlpatterns = [path("", views.StackList.as_view(), name="stack_list")]
>>>>>>> develop
