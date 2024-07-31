from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserStackList.as_view(), name="user_stack_list"),
    path(
        "create/",
        views.UserStackCreate.as_view(),
        name="user_stack_create",
    ),
    path(
        "delete/<int:user_stack_id>/",
        views.UserStackDelete.as_view(),
        name="user_stack_delete",
    ),
]
