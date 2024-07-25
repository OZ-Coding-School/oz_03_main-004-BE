from django.urls import path
from .views import AttendanceViewSet

urlpatterns = [
    # 출석 기록을 조회하는 엔드포인트
    path("", AttendanceViewSet.as_view({"get": "list"}), name="attendance-list"),
    # 출석을 처리하는 엔드포인트
    path(
        "increment/",
        AttendanceViewSet.as_view({"post": "increment"}),
        name="attendance-increment",
    ),
    # 출석 기록에서 코인을 차감하는 엔드포인트
    path(
        "decrement/",
        AttendanceViewSet.as_view({"post": "decrement"}),
        name="attendance-decrement",
    ),
]
