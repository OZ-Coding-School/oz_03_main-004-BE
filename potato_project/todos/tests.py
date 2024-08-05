import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Todo


class TodoAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.todo = Todo.objects.create(
            user_id=self.user, task="Test Task", is_done=False, date=timezone.now()
        )

    def test_create_todo(self):
        data = {
            "user_id": self.user.id,
            "task": "New Task",
            "is_done": False,
            "date": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        response = self.client.post(
            reverse("todo-list-create"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 2)

    def test_get_todo_list(self):
        response = self.client.get(reverse("todo-list-create"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["todos"]), 1)

    def test_get_todo_detail(self):
        response = self.client.get(reverse("todo-detail", args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["task"], "Test Task")

    def test_update_todo(self):
        data = {
            "task": "Updated Task",
            "is_done": True,
            "date": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        response = self.client.put(
            reverse("todo-detail", args=[self.todo.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.task, "Updated Task")
        self.assertTrue(self.todo.is_done)

    def test_delete_todo(self):
        response = self.client.delete(reverse("todo-detail", args=[self.todo.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Todo.objects.count(), 0)
