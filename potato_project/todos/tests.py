from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

from .models import Todo


class TodoCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("todo-create")

    def test_create_todo_success(self):
        data = {"task": "Test Task", "date": "2024-09-01"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo_id = response.data.get("id")
        self.assertIsNotNone(todo_id, "Todo ID should be in the response")
        todo = Todo.objects.get(id=todo_id)
        self.assertEqual(todo.task, "Test Task")
        self.assertEqual(str(todo.date), "2024-09-01")

    def test_create_todo_invalid_date(self):
        data = {"task": "Test Task", "date": "invalid-date"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
