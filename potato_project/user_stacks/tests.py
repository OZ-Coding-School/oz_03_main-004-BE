from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import User

from .models import Stack, UserStack
from .serializers import UserStackSerializer


class UserStackListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 스택과 유저 스택 생성
        self.stack1 = Stack.objects.create(name="Django")
        self.stack2 = Stack.objects.create(name="React")
        self.user_stack1 = UserStack.objects.create(user=self.user, stack=self.stack1)
        self.user_stack1 = UserStack.objects.create(user=self.user, stack=self.stack2)

        self.url = reverse("user_stack_list")

    def test_get_user_stacks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stacks = UserStack.objects.filter(user=self.user)
        serializer = UserStackSerializer(stacks, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_get_user_stacks_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
