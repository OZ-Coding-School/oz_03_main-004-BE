from django.urls import path

from .views import (DailyTodoListView, MonthlyCompletedTodosView,
                    TodayTodoListView, TodoCreateView, TodoDeleteView,
                    TodoMarkDoneView, TodoMarkUndoneView, TodoUpdateView)

urlpatterns = [
    path("create/", TodoCreateView.as_view(), name="todo-create"),
    path("<int:id>/update/", TodoUpdateView.as_view(), name="todo-update"),
    path("<int:id>/delete/", TodoDeleteView.as_view(), name="todo-delete"),
    path("<int:id>/done/", TodoMarkDoneView.as_view(), name="todo-mark-done"),
    path("<int:id>/undone/", TodoMarkUndoneView.as_view(), name="todo-mark-undone"),
    path("today/", TodayTodoListView.as_view(), name="todo-today"),
    path(
        "<str:date>/", DailyTodoListView.as_view(), name="todo-daily"
    ),  # 'YYYY-MM-DD' 형식
    path(
        "completed/<int:year>/<int:month>/",
        MonthlyCompletedTodosView.as_view(),
    ),
]
