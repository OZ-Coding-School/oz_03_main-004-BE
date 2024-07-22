from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Attendance
from .serializers import AttendanceSerializer
from django.utils import timezone

User = get_user_model()

class AttendanceViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.attendance_url = reverse("attendance-list")
        self.increment_url = reverse("attendance-increment")
        self.decrement_url = reverse("attendance-decrement")

    def test_list_attendance_no_record(self):
        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"출석 기록이 없습니다."})

    def test_list_attendance_with_record(self):
        Attendance.objects.create(user_id=self.user, date=timezone.now().date(), coin_awarded=1)
        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        attendance = Attendance.objects.filter(user_id=self.user).order_by("-date").first()
        serializer = AttendanceSerializer(attendance)
        self.assertEqual(response.data, serializer.data)

    def test_increment_attendance_first_time(self):
        response = self.client.post(self.increment_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attendance = Attendance.objects.get(user_id=self.user)
        self.assertEqual(attendance.coin_awarded, 1)

    def test_increment_attendance_already_done_today(self):
        Attendance.objects.create(user_id=self.user, date=timezone.now().date(), coin_awarded=1)
        response = self.client.post(self.increment_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"오늘은 출석을 이미 하셨어요!"})

    def test_decrement_attendance_no_record(self):
        response = self.client.post(self.decrement_url, {"value": 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"message": "출석 기록이 없습니다."})

    def test_decrement_attendance_insufficient_coins(self):
        Attendance.objects.create(user_id=self.user, date=timezone.now().date(), coin_awarded=1)
        response = self.client.post(self.decrement_url, {"value": 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "코인이 모자라요!"})

    def test_decrement_attendance_success(self):
        Attendance.objects.create(user_id=self.user, date=timezone.now().date(), coin_awarded=5)
        response = self.client.post(self.decrement_url, {"value": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        attendance = Attendance.objects.get(user_id=self.user)
        self.assertEqual(attendance.coin_awarded, 2)
        self.assertEqual(response.data, {"message": "물건을 구매했습니다.", "coin_awarded": 2})
