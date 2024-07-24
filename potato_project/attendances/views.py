# attendances/views.py
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ViewSet):
    # 가장 최근 출석기록을 가져오는 함수
    def get_user_attendance(self, user):
        # 날짜를 기준으로 내림차순하여 첫번째 날짜를 가저욤
        return Attendance.objects.filter(user_id=user).order_by("-date").first()

    # 출석기록을 조회하고 정보를 시리얼라이즈하여 반환하는 역할
    def list(self, request):
        user = request.user
        attendance = self.get_user_attendance(user)
        if attendance:
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)
        else:
            return Response({"출석 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 사용자 출석을 처리하고, 매일 한번 출석하도록 제한하는 기능
    @action(detail=False, methods=["post"])
    def increment(self, request):
        user = request.user
        today = timezone.now().date()

        # 출석날짜가 오늘이면 이미 출석함을 반환
        attendance = self.get_user_attendance(user)
        if attendance and attendance.date == today:
            return Response({"오늘은 출석을 이미 하셨어요!"}, status=status.HTTP_400_BAD_REQUEST)

        new_attendance = Attendance.objects.create(
            user_id=user, date=today, coin_awarded=1
        )

        serializer = AttendanceSerializer(new_attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 더미 함수, 이후 코인샾이 등장할 경우 코인 차감이 가능하게 하는 함수

    @action(detail=False, methods=["post"])
    def decrement(self, request):
        user = request.user
        decrement_value = int(request.data.get("value", 1))  # 차감할 값, 기본은 1

        # 사용자의 출석 기록 조회
        attendance = self.get_user_attendance(user)
        if not attendance:
            return Response(
                {"message": "출석 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        # 차감하려는 코인량이 현재 코인량보다 많으면 실패 응답 반환
        if attendance.coin_awarded < decrement_value:
            return Response(
                {"message": "코인이 모자라요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 코인 차감 처리
        attendance.coin_awarded -= decrement_value
        attendance.save()

        # 성공 응답 반환
        return Response(
            {"message": "물건을 구매했습니다.", "coin_awarded": attendance.coin_awarded}
        )
