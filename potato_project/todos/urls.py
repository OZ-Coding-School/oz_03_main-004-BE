from django.urls import path
from .views import TodoView

urlpatterns = [
    path("todos/", TodoView.as_view(), name="todo-list-create"),
    path("todos/<int:todo_id>/", TodoView.as_view(), name="todo-detail"),
]
