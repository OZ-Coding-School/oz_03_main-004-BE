from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from stacks.models import Stack
from stacks.serializers import StackSerializer
from users.models import User


class StackListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="kingtato", nickname="kingtato")
        self.client.force_authenticate(user=self.user)

        self.stack1 = Stack.objects.create(name="Python")
        self.stack2 = Stack.objects.create(name="Java")

        self.url = "/stacks/all"

    def test_get_stack_list_success(self):
        response = self.client.get(self.url)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터 확인
        response_data = response.json()
        expected_data = StackSerializer([self.stack1, self.stack2], many=True).data
        self.assertEqual(response_data, expected_data)
