from django.urls import path

from . import views


urlpatterns = [
    path("<int:user_id>/", views.UserStackList.as_view(), name="user_stack_list"),
    path("<int:user_id>/create/", views.UserStackCreate.as_view(), name="user_stack_create"),
    path("<int:user_id>/patch/", views.UserStackPacth.as_view(), name="user_stack_patch"),
]