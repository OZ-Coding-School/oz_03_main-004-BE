from datetime import datetime, timedelta

from django.db.models import Case, Count, IntegerField, When
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date = self.request.query_params.get("date", timezone.now().date())
        return Todo.objects.filter(user=self.request.user, date__date=date)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoToggleView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_done = not instance.is_done
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MonthlyCompletionRateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(
            days=1
        )

        daily_rates = (
            Todo.objects.filter(user=request.user, date__range=(start_date, end_date))
            .values("date__date")
            .annotate(
                total=Count("id"),
                completed=Count(
                    Case(When(is_done=True, then=1), output_field=IntegerField())
                ),
            )
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


class TodayTodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return Todo.objects.filter(user=self.request.user, date__date=today)
