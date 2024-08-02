from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import User

from .models import Todo

User = get_user_model()


class TodoCreateViewTests(TestCase):
    def setUp(self):
        # 초기 설정: 테스트 유저 및 API 클라이언트 인증 설정
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("todo-create")

    def test_create_todo_success(self):
        # 성공적인 투두 항목 생성 테스트
        data = {"task": "Test Todo", "date": "2024-08-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 응답 데이터를 통해 데이터베이스에 객체가 생성되었는지 확인
        created_todo = Todo.objects.filter(task="Test Todo", user=self.user).first()
        self.assertIsNotNone(created_todo, "Todo should be created in the database")
        self.assertEqual(created_todo.task, "Test Todo")
        self.assertEqual(str(created_todo.date), "2024-08-01")

    def test_create_todo_invalid_date(self):
        # 유효하지 않은 날짜 형식으로 투두 항목 생성 실패 테스트
        data = {"task": "Test Task", "date": "invalid-date"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class TodoUpdateViewTests(APITestCase):
    def setUp(self):
        # 초기 설정: 테스트 유저, API 클라이언트 인증 및 테스트 투두 항목 생성
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            task="Initial Task", date="2024-08-01", user=self.user
        )
        self.url = reverse("todo-update", kwargs={"id": self.todo.id})

    def test_update_todo_success(self):
        # 성공적인 투두 항목 업데이트 테스트
        updated_data = {"task": "Updated Task", "date": "2024-09-01"}
        response = self.client.put(self.url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task, "Updated Task")
        self.assertEqual(str(self.todo.date), "2024-09-01")


class TodoDeleteViewTests(TestCase):
    def setUp(self):
        # 초기 설정: 테스트 유저, API 클라이언트 인증 및 테스트 투두 항목 생성
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            task="Test Task", date="2024-08-01", user=self.user
        )
        self.url = reverse("todo-delete", kwargs={"id": self.todo.id})

    def test_delete_todo_success(self):
        # 성공적인 투두 항목 삭제 테스트
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_delete_todo_not_found(self):
        # 존재하지 않는 투두 항목 삭제 시도 테스트
        non_existing_id = self.todo.id + 1
        url = reverse("todo-delete", kwargs={"id": non_existing_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_unauthenticated(self):
        # 인증되지 않은 사용자가 투두 항목 삭제 시도 시 실패 테스트
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TodoMarkDoneViewTests(APITestCase):
    def setUp(self):
        # 초기 설정: 테스트 유저 및 API 클라이언트 인증 설정
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            task="Test Task", date="2024-08-01", user=self.user, is_done=False
        )
        self.url = reverse("todo-mark-done", kwargs={"id": self.todo.id})

    def test_mark_todo_done_success(self):
        # 성공적인 투두 항목 상태 변경 테스트 (is_done: False -> True
        response = self.client.patch(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_done)

    def test_mark_todo_done_unauthenticated(self):
        # 인증되지 않은 사용자가 투두 항목 상태 변경 시도 시 실패 테스트
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_todo_done_not_found(self):
        # 존재하지 않는 투두 항목 상태 변경 시도 테스트
        non_existing_id = self.todo.id + 1
        url = reverse("todo-mark-done", kwargs={"id": non_existing_id})
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
