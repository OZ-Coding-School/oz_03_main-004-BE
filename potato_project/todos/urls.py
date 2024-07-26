from django.urls import path

from .views import (
    DailyTodoListView,
    MonthlyCompletionRateView,
    TodayTodoListView,
    TodoCreateView,
    TodoDeleteView,
    TodoToggleView,
    TodoUpdateView,
)

urlpatterns = [
    path("todos/create/", TodoCreateView.as_view()),
    path("todos/<int:pk>/update/", TodoUpdateView.as_view()),
    path("todos/<int:pk>/delete/", TodoDeleteView.as_view()),
    path("todos/<int:pk>/toggle/", TodoToggleView.as_view(), name="todo-toggle"),
    path("todos/today/", TodayTodoListView.as_view()),
    path("todos/<str:date>/", DailyTodoListView.as_view()),  # 'YYYY-MM-DD' 형식
    path(
        "todos/completion_rate/<int:year>/<int:month>/",
        MonthlyCompletionRateView.as_view(),
    ),
]
