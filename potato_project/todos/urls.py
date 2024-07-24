from django.urls import path
from .views import TodoView

urlpatterns = [
    path("", TodoView.as_view(), name="todo_list"),  # GET 요청: /todos/
    path(
        "<int:todo_id>/", TodoView.as_view(), name="todo_detail"
    ),  # GET 요청: /todos/<todo_id>/
    path(
        "completion_percentage/", TodoView.as_view(), name="completion_percentage_all"
    ),  # GET 요청: /todos/completion_percentage/
    path(
        "completion_percentage/<int:user_id>/",
        TodoView.as_view(),
        name="completion_percentage_user",
    ),  # GET 요청: /todos/completion_percentage/<user_id>/
]
