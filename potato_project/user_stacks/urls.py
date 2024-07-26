from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserStackList.as_view(), name="user_stack_list"),
    path(
        "create/",
        views.UserStackCreate.as_view(),
        name="user_stack_create",
    ),
    path("patch/", views.UserStackPatch.as_view(), name="user_stack_patch"),
    path("delete/", views.UserStackDelete.as_view(), name="user_stack_delete"),
]
