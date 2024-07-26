from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoCreateSerializer, TodoSerializer

# ... (IsAuthenticated, TodayTodoListView, MonthlyCompletionRateView는 동일)


# 1. 투두리스트 항목 생성 (UI에서 입력 받은 데이터 + 선택된 날짜로 생성)
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        date_str = self.request.data.get("date")  # 프론트엔드에서 전달된 날짜 문자열
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid date format or missing date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, date=date)


# 2. 투두리스트 항목 수정 (UI에서 입력 받은 데이터 + 선택된 날짜로 수정)
class TodoUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_update(self, serializer):
        date_str = self.request.data.get("date")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid date format or missing date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(date=date)


# 3. 투두리스트 항목 삭제
class TodoDeleteView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


# 4. 투두리스트 is_done True<->False
class TodoMarkDoneView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.is_done = True  # O 버튼 클릭 시 is_done을 True로 변경
        serializer.instance.save()


class TodoMarkUndoneView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

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
        today = timezone.now().date()
        return Todo.objects.filter(user=self.request.user, date__date=today)


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

        return Todo.objects.filter(user=self.request.user, date__date=date)


# 7. 월별 투두리스트 완료율 조회
class MonthlyCompletionRateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(
            days=1
        )

        todos = Todo.objects.filter(
            user=request.user, date__range=(start_date, end_date)
        )

        daily_rates = (
            todos.values("date__date")
            .annotate(total=Count("id"), completed=Count(Q(is_done=True)))
            .order_by("date__date")
        )

        rates = {
            str(item["date__date"]): (
                round(item["completed"] / item["total"] * 100, 2)
                if item["total"] > 0
                else 0
            )
            for item in daily_rates
        }

        return Response(rates)
