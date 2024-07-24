from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Attendance

class AttendanceViewSetTests(TestCase):
    def setUp(self):
        # 테스트에 사용할 사용자 생성
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
    
    def test_list_attendance_no_record(self):
        # 출석 기록이 없는 경우
        response = self.client.get('/attendances/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"출석 기록이 없습니다."})
    
    def test_increment_attendance(self):
        # 출석 기록을 추가
        response = self.client.post('/attendances/increment/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['coin_awarded'], 1)
    
    def test_increment_attendance_already_exists(self):
        # 출석 기록이 이미 있는 경우
        today = timezone.now().date()
        Attendance.objects.create(user=self.user, date=today, coin_awarded=1)
        
        response = self.client.post('/attendances/increment/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"오늘은 출석을 이미 하셨어요!"})
    
    def test_decrement_attendance_no_record(self):
        # 출석 기록이 없는 경우 코인 차감 시도
        response = self.client.post('/attendances/decrement/', {'value': 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"message": "출석 기록이 없습니다."})
    
    def test_decrement_attendance_insufficient_coins(self):
        # 출석 기록이 있지만 코인이 부족한 경우
        Attendance.objects.create(user=self.user, date=timezone.now().date(), coin_awarded=1)
        
        response = self.client.post('/attendances/decrement/', {'value': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "코인이 모자라요!"})
    
    def test_decrement_attendance_success(self):
        # 출석 기록이 있고 충분한 코인이 있는 경우
        Attendance.objects.create(user=self.user, date=timezone.now().date(), coin_awarded=5)
        
        response = self.client.post('/attendances/decrement/', {'value': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "물건을 구매했습니다.")
        self.assertEqual(response.data['coin_awarded'], 3)
