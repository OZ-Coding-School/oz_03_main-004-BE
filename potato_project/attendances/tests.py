from datetime import date

from attendances.models import Attendance
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class AttendanceViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", email="testuser@example.com"
        )

    def test_create_attendance(self):
        # 출석 기록 생성
        attendance = Attendance.objects.create(
            user=self.user, date=date.today(), coin_awarded=10
        )
        self.assertEqual(attendance.user, self.user)
        self.assertEqual(attendance.date, date.today())
        self.assertEqual(attendance.coin_awarded, 10)

    def test_read_attendance(self):
        # 출석 기록 생성
        Attendance.objects.create(user=self.user, date=date.today(), coin_awarded=10)
        attendance = Attendance.objects.get(user=self.user, date=date.today())
        self.assertEqual(attendance.user.username, "testuser")
        self.assertEqual(attendance.coin_awarded, 10)

    def test_update_attendance(self):
        # 출석 기록 생성 및 수정
        attendance = Attendance.objects.create(
            user=self.user, date=date.today(), coin_awarded=10
        )
        attendance.coin_awarded = 20
        attendance.save()
        updated_attendance = Attendance.objects.get(user=self.user, date=date.today())
        self.assertEqual(updated_attendance.coin_awarded, 20)

    def test_delete_attendance(self):
        # 출석 기록 생성 및 삭제
        attendance = Attendance.objects.create(
            user=self.user, date=date.today(), coin_awarded=10
        )
        attendance_id = attendance.id
        attendance.delete()
        with self.assertRaises(Attendance.DoesNotExist):
            Attendance.objects.get(id=attendance_id)
