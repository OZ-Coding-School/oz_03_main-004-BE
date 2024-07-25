# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.TodayTodoListView.as_view(), name="today_todo_list"),
    path("list/", views.TodoListCreateView.as_view(), name="todo_list_create"),
    path(
        "detail/<int:pk>/",
        views.TodoRetrieveUpdateDestroyView.as_view(),
        name="todo_detail",
    ),
    path("toggle/<int:pk>/", views.TodoToggleView.as_view(), name="todo_toggle"),
    path(
        "monthly-rate/<int:year>/<int:month>/",
        views.MonthlyCompletionRateView.as_view(),
        name="monthly_completion_rate",
    ),
]
