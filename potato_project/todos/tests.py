from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, force_authenticate
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


class TodoMarkUndoneViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            task="Test Task", date="2024-08-01", is_done=True, user=self.user
        )
        self.url = reverse("todo-mark-undone", kwargs={"id": self.todo.id})

    def test_mark_todo_undone_success(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_done)

    def test_mark_todo_undone_not_found(self):
        non_existing_id = self.todo.id + 1
        url = reverse("todo-mark-undone", kwargs={"id": non_existing_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_todo_undone_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TodayTodoListViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.today = timezone.localtime(timezone.now()).date()

        # 오늘의 할 일 생성
        self.todo_today_1 = Todo.objects.create(
            task="Today's Task 1", date=self.today, user=self.user
        )
        self.todo_today_2 = Todo.objects.create(
            task="Today's Task 2", date=self.today, user=self.user
        )

        # 다른 날짜의 할 일 생성
        self.other_date = self.today - timezone.timedelta(days=1)
        self.todo_other_day = Todo.objects.create(
            task="Other Day Task", date=self.other_date, user=self.user
        )

        self.url = reverse("todo-today")

    def test_get_today_todos_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["task"], self.todo_today_1.task)
        self.assertEqual(response.data[1]["task"], self.todo_today_2.task)

    def test_get_today_todos_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DailyTodoListViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

        self.target_date = datetime.now().date()
        self.url = reverse(
            "todo-daily", kwargs={"date": self.target_date.strftime("%Y-%m-%d")}
        )

        # 생성된 날짜의 할 일
        self.todo_on_date_1 = Todo.objects.create(
            task="Task 1", date=self.target_date, user=self.user
        )
        self.todo_on_date_2 = Todo.objects.create(
            task="Task 2", date=self.target_date, user=self.user
        )

        # 다른 날짜의 할 일
        self.other_date = self.target_date - timedelta(days=1)
        self.todo_other_day = Todo.objects.create(
            task="Other Task", date=self.other_date, user=self.user
        )

    def test_get_todos_valid_date(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        todo_tasks = {todo["task"] for todo in response.data}
        self.assertIn(self.todo_on_date_1.task, todo_tasks)
        self.assertIn(self.todo_on_date_2.task, todo_tasks)

    def test_get_todos_invalid_date(self):
        invalid_url = reverse("todo-daily", kwargs={"date": "invalid-date"})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_todos_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MonthlyCompletedTodosViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)

        self.year = 2024
        self.month = 8
        self.url = reverse(
            "todo-monthly", kwargs={"year": self.year, "month": self.month}
        )

        # 테스트 데이터를 생성
        self.start_date = date(self.year, self.month, 1)
        self.end_date = date(self.year, self.month + 1, 1) - timedelta(days=1)

        # 해당 월의 완료된 할 일 생성
        for i in range(5):
            Todo.objects.create(
                task=f"Completed Task {i}",
                date=self.start_date + timedelta(days=i),
                user=self.user,
                is_done=True,
            )

        # 해당 월의 완료되지 않은 할 일 생성
        for i in range(5, 10):
            Todo.objects.create(
                task=f"Not Completed Task {i}",
                date=self.start_date + timedelta(days=i),
                user=self.user,
                is_done=False,
            )

        # 다른 달의 완료된 할 일 생성
        Todo.objects.create(
            task="Other Month Task",
            date=self.start_date - timedelta(days=1),
            user=self.user,
            is_done=True,
        )

    def test_get_monthly_completed_todos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        completed_counts = response.data["completed_todos"]
        self.assertEqual(len(completed_counts), 5)  # 5일의 할 일 완료

        for i in range(5):
            self.assertIn(str(self.start_date + timedelta(days=i)), completed_counts)
            self.assertEqual(
                completed_counts[str(self.start_date + timedelta(days=i))], 1
            )

    def test_get_monthly_completed_todos_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
