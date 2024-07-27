from django.urls import path

from .views import (DailyTodoListView, MonthlyCompletionRateView,
                    TodayTodoListView, TodoCreateView, TodoDeleteView,
                    TodoMarkDoneView, TodoMarkUndoneView, TodoUpdateView)

urlpatterns = [
    path("create/", TodoCreateView.as_view()),
    path("<int:pk>/update/", TodoUpdateView.as_view()),
    path("<int:pk>/delete/", TodoDeleteView.as_view()),
    path("todos/<int:pk>/done/", TodoMarkDoneView.as_view(), name="todo-mark-done"),
    path(
        "todos/<int:pk>/undone/", TodoMarkUndoneView.as_view(), name="todo-mark-undone"
    ),
    path("today/", TodayTodoListView.as_view()),
    path("<str:date>/", DailyTodoListView.as_view()),  # 'YYYY-MM-DD' 형식
    path(
        "completion_rate/<int:year>/<int:month>/",
        MonthlyCompletionRateView.as_view(),
    ),
]
