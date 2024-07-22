from django.urls import path

from . import views


urlpatterns = [
    path("<int:user_id>/", views.UserStackList.view_as(), name="user_stack_list"),
    path("<int:user_id>/create/", views.UserStackCreate.view_as(), name="user_stack_create"),
    path("<int:user_id>/patch/", views.UserStackPacth.view_as(), name="user_stack_patch"),
]