from datetime import date, datetime, timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoCreateSerializer, TodoSerializer


# 1. 투두리스트 항목 생성 (UI에서 입력 받은 데이터 + 선택된 날짜로 생성)
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        date_str = self.request.data.get("date")  # 프론트엔드에서 전달된 날짜 문자열
        try:
            # datetime 객체 생성
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid date format or missing date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, date=date)


# 2. 투두리스트 항목 수정 (UI에서 입력 받은 데이터 + 선택된 날짜로 수정)
class TodoUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        todo_id = self.kwargs.get("id")
        return get_object_or_404(Todo, id=todo_id, user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_update(self, serializer):
        date_str = self.request.data.get("date")
        try:
            # datetime 객체 생성
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            serializer.save(date=date)  # serializer에 날짜 저장
        except (ValueError, TypeError):
            raise ValidationError({"error": "Invalid date format or missing date."})


# 3. 투두리스트 항목 삭제
class TodoDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        todo_id = self.kwargs.get("id")
        return get_object_or_404(Todo, id=todo_id, user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


# 4. 투두리스트 is_done True<->False
class TodoMarkDoneView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    http_method_names = ["patch"]  # PATCH 메서드만 허용

    def get_object(self):
        todo_id = self.kwargs.get("id")
        return get_object_or_404(Todo, id=todo_id, user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.is_done = True  # O 버튼 클릭 시 is_done을 True로 변경
        serializer.instance.save()


class TodoMarkUndoneView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    http_method_names = ["patch"]  # PATCH 메서드만 허용

    def get_object(self):
        todo_id = self.kwargs.get("id")

        return get_object_or_404(Todo, id=todo_id, user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.is_done = False  # X 버튼 클릭 시 is_done을 False로 변경
        serializer.instance.save()


# 5. 오늘 날짜 투두리스트 조회
class TodayTodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        return Todo.objects.filter(user=self.request.user, date=today)


# 6. 특정 날짜 투두리스트 조회 (캘린더에서 선택한 날짜 기준)
class DailyTodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date_str = self.kwargs["date"]
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Todo.objects.none()  # 유효하지 않은 날짜면 빈 쿼리셋 반환

        return Todo.objects.filter(user=self.request.user, date=date)


# 7. 월별 투두리스트 완료 개수 조회
class MonthlyCompletedTodosView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]

        # DateField를 사용하므로 start_date와 end_date를 date 객체로 생성
        start_date = date(year, month, 1)
        # 다음 달 1일에서 하루를 빼서 해당 월의 마지막 날을 계산
        end_date = date(year, month + 1, 1) - timedelta(days=1)

        todos = Todo.objects.filter(
            user=request.user, date__range=(start_date, end_date), is_done=True
        )

        # 날짜별 완료 개수를 계산
        daily_completed_counts = (
            todos.values("date").annotate(completed_count=Count("id")).order_by("date")
        )

        completed_counts = {
            "user_id": request.user.id,
            "completed_todos": {
                str(item["date"]): item["completed_count"]
                for item in daily_completed_counts
            },
        }

        return Response(completed_counts)
