# attendances/views.py
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from users.models import User


class AttendanceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # 가장 최근 출석기록을 가져오는 함수
    def get_user_attendance(self, user):
        # 날짜를 기준으로 내림차순하여 첫번째 날짜를 가져옴
        return Attendance.objects.filter(user=user).order_by("-date").first()

    # 모든 출석 기록을 반환하는 함수
    def list(self, request):
        user = request.user
        # 사용자의 모든 출석 기록을 가져옴
        attendance_records = Attendance.objects.filter(user=user).order_by("-date")
        if attendance_records.exists():
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "출석 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

    # 사용자 출석을 처리하고, 매일 한번 출석하도록 제한하는 기능
    @action(detail=False, methods=["post"])
    def increment(self, request):
        user = request.user
        today = timezone.now().date()

        # 출석날짜가 오늘이면 이미 출석함을 반환
        attendance = self.get_user_attendance(user)
        if attendance and attendance.date == today:
            return Response({"오늘은 출석을 이미 하셨어요!"}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 출석 기록 생성
        new_attendance = Attendance.objects.create(
            user=user, date=today, coin_awarded=1
        )

        # 총 코인 수 업데이트
        user.total_coins += 1
        user.save()

        serializer = AttendanceSerializer(new_attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 더미 함수, 이후 코인샵이 등장할 경우 코인 차감이 가능하게 하는 함수
    @action(detail=False, methods=["post"])
    def decrement(self, request):
        user = request.user
        decrement_value = int(request.data.get("value", 1))  # 차감할 값, 기본은 1

        # 사용자의 출석 기록 조회
        if user.total_coins < decrement_value:
            return Response(
                {"message": "코인이 모자라요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 코인 차감 처리
        user.total_coins -= decrement_value
        user.save()

        # 성공 응답 반환
        return Response(
            {"message": "물건을 구매했습니다.", "total_coins": user.total_coins}
        )
